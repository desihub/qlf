import os
import sys
import io
from log import setup_logger
import subprocess
import datetime
import configparser
import shutil
import logging
from multiprocessing import Manager, Lock
from threading import Thread
from qlf_models import QLFModels

qlf_root = os.getenv('QLF_ROOT')
cfg = configparser.ConfigParser()

try:
    cfg.read('%s/framework/config/qlf.cfg' % qlf_root)
    qlconfig = cfg.get('main', 'qlconfig')
    logmain = cfg.get('main', 'logfile')
    desi_spectro_redux = cfg.get('namespace', 'desi_spectro_redux')
except Exception as error:
    print(error)
    print("Error reading  %s/framework/config/qlf.cfg" % qlf_root)
    sys.exit(1)

logger = logging.getLogger("main_logger")


class QLFProcess(object):
    """ Class responsible for managing Quick Look pipeline process. """

    def __init__(self, data):
        self.pipeline_name = 'Quick Look'
        self.data = data
        self.models = QLFModels()

        output_dir = os.path.join(
            'exposures',
            self.data.get('night'),
            self.data.get('zfill')
        )

        output_full_dir = os.path.join(desi_spectro_redux, output_dir)

        # Remove old dir
        if os.path.isdir(output_full_dir):
            shutil.rmtree(output_full_dir)

        # Make output dir
        os.makedirs(output_full_dir)

        self.data['output_dir'] = output_dir
        self.logger = setup_logger(
            'pipe-{}'.format(self.data.get('expid')),
            '{}/expid.{}.log'.format(output_full_dir, self.data.get('expid'))
        )

    def start_process(self):
        """ Start pipeline. """

        self.logger.info('Started %s ...' % self.pipeline_name)
        self.logger.info('Night: %s' % self.data.get('night'))
        self.logger.info('Exposure: %s' % str(self.data.get('expid')))

        self.data['start'] = datetime.datetime.now().replace(microsecond=0)

        # create process in database and obtain the process id
        process = self.models.insert_process(
            self.data,
            self.pipeline_name
        )

        self.data['process_id'] = process.id
        self.data['status'] = process.status

        # TODO: ingest configuration file used, this should be done by process
        # self.models.insert_config(process.id)

        self.logger.info('Process ID: %i' % process.id)

    def finish_process(self):
        """ Finish pipeline. """

        self.data['end'] = datetime.datetime.now().replace(microsecond=0)

        self.data['duration'] = str(self.data.get('end') - self.data.get('start'))

        self.logger.info("Process with expID {} completed in {}.".format(
           self.data.get('expid'),
           self.data.get('duration')
        ))

        self.models.update_process(
            process_id=self.data.get('process_id'),
            end=self.data.get('end'),
            process_dir=self.data.get('output_dir'),
            status=self.data.get('status')
        )


class Jobs(QLFProcess):

    def __init__(self, data):
        super().__init__(data)
        self.num_cameras = len(self.data.get('cameras'))

        # TODO: improvements - get stages/steps in database
        self.stages = [
            {"display_name": "Initialize", "regex": "Starting to run step Initialize", "count": 0},
            {"display_name": "Preprocessing", "regex": "Starting to run step Preproc", "count": 0},
            {"display_name": "Boxcar Extraction", "regex": "Starting to run step BoxcarExtract", "count": 0},
            {"display_name": "Sky Subtraction", "regex": "Starting to run step SkySub", "count": 0},
            {"display_name": "Pipeline completed", "regex": "Pipeline completed.", "count": 0}
        ]

    def start_jobs(self):
        """ Distributes the cameras for parallel processing. """

        procs = list()
        return_cameras = Manager().list()
        resumelog_lock = Lock()

        for camera in self.data.get('cameras'):
            camera['start'] = datetime.datetime.now().replace(
                microsecond=0
            )

            logname = os.path.join(
                self.data.get('output_dir'),
                "run-%s.log" % camera.get('name')
            )

            camera['logname'] = logname

            job = self.models.insert_job(
                process_id=self.data.get('process_id'),
                camera=camera.get('name'),
                start=camera.get('start'),
                logname=camera.get('logname')
            )

            camera['job_id'] = job.id

            args = (
                self.data,
                camera,
                return_cameras,
                resumelog_lock,
            )

            proc = Thread(target=self.start_parallel_job, args=args)
            proc.start()
            procs.append(proc)

        for proc in procs:
            proc.join()

        self.data['cameras'] = return_cameras

        self.logger.info('Begin ingestion of results...')
        start_ingestion = datetime.datetime.now().replace(microsecond=0)

        # TODO: refactor?
        camera_failed = 0

        for camera in self.data.get('cameras'):
            output_path = os.path.join(
                desi_spectro_redux,
                self.data.get('output_dir'),
                'ql-*-%s-%s.yaml' % (
                    camera.get('name'),
                    self.data.get('zfill')
                )
            )

            self.models.update_job(
                job_id=camera.get('job_id'),
                end=camera.get('end'),
                status=camera.get('status'),
                output_path=output_path
            )

            if not camera.get('status') == 0:
                camera_failed += 1

        status = 0

        if camera_failed > 0:
            status = 1

        self.data['status'] = status

        duration_ingestion = str(
            datetime.datetime.now().replace(microsecond=0) - start_ingestion
        )

        self.logger.info("Results ingestion complete in %s." % duration_ingestion)

    def start_parallel_job(self, data, camera, return_cameras, lock):
        """ Execute QL Pipeline by camera """

        cmd = [
            'desi_quicklook',
            '-i', qlconfig,
            '-n', data.get('night'),
            '-c', camera.get('name'),
            '-e', str(data.get('expid')),
            '--rawdata_dir', data.get('desi_spectro_data'),
            '--mergeQA',
            '--specprod_dir', desi_spectro_redux
        ]

        log_path = os.path.join(desi_spectro_redux, camera.get('logname'))

        logname = io.open(os.path.join(
                desi_spectro_redux,
                camera.get('logname')
        ), 'wb')

        cwd = os.path.join(
            desi_spectro_redux,
            data.get('output_dir')
        )

        with subprocess.Popen(cmd, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, cwd=cwd) as process:
            while process.poll() is None:
                line = process.stdout.readline()
                if not line:
                    break
                self.resume_log(line, camera.get('name'), data.get('expid'), lock)
                logname.write(line)
                logname.flush()

            retcode = process.wait()

        logname.close()

        camera['end'] = datetime.datetime.now().replace(microsecond=0)
        camera['status'] = 0
        camera['duration'] = str(
            camera.get('end') - camera.get('start')
        )

        if retcode < 0:
            camera['status'] = 1

        return_cameras.append(camera)

    def resume_log(self, line, camera, expid, lock):
        """ """

        lock.acquire()

        try:
            line = line.decode("utf-8").replace('\n', '')
            line_str = line.split(':')[-1]

            if line.find('ERROR') > -1:
                self.logger.error("ERROR: Camera {}: {}".format(camera, line_str))
            elif line.find('CRITICAL') > -1:
                self.logger.critical("CRITICAL: Camera {}: {}".format(camera, line_str))
            else:
                for stage in self.stages:
                    if line.find(stage.get('regex')) > -1:
                        stage['count'] += 1
                        break

                for stage in self.stages:
                    if line.find(stage.get('regex')) > -1:
                        last_stage = None
                        index = self.stages.index(stage) - 1
                        if index > -1:
                            last_stage = self.stages[index]

                        if stage.get('count') == self.num_cameras:
                            if last_stage and last_stage.get('count') != self.num_cameras:
                                self.logger.error("ERROR: stage '{}' did not end as expected.".format(
                                    last_stage.get("display_name")))

                            self.logger.info(stage.get('regex'))

        except Exception as err:
            self.logger.info(err)

        lock.release()


if __name__ == "__main__":
    print('Standalone execution...')
