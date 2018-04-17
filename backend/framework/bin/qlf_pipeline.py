import os
import io
from log import setup_logger
import subprocess
import datetime
import configparser
import shutil
import logging
from multiprocessing import Manager, Lock, Process
from threading import Thread
from qlf_models import QLFModels

qlf_root = os.getenv('QLF_ROOT')
cfg = configparser.ConfigParser()

cfg.read('%s/framework/config/qlf.cfg' % qlf_root)
qlconfig = cfg.get('main', 'qlconfig')
logmain = cfg.get('main', 'logfile')
logpipeline = cfg.get('main', 'logpipeline')
desi_spectro_redux = cfg.get('namespace', 'desi_spectro_redux')

logger = logging.getLogger("main_logger")
pipe_logger = setup_logger(
    'logpipeline', logpipeline
)


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

    def start_process(self):
        """ Start pipeline. """

        pipe_logger.info('Night {}'.format(self.data.get('night')))

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

        pipe_logger.info('Process ID {}'.format(process.id))
        pipe_logger.info('ExpID {} started.'.format(self.data.get('expid')))

        return process.id

    def finish_process(self):
        """ Finish pipeline. """

        self.data['end'] = datetime.datetime.now().replace(microsecond=0)

        self.data['duration'] = self.data.get('end') - self.data.get('start')

        pipe_logger.info("ExpID {} ended (runtime: {}).".format(
           self.data.get('expid'),
           str(self.data.get('duration'))
        ))

        self.models.update_process(
            process_id=self.data.get('process_id'),
            end=self.data.get('end'),
            process_dir=self.data.get('output_dir'),
            status=self.data.get('status')
        )

        proc = Thread(target=self.ingest_parallel_qas)
        proc.start()


class Jobs(QLFProcess):

    def __init__(self, data):

        super().__init__(data)
        self.num_cameras = len(self.data.get('cameras'))

        # TODO: improvements - get stages/steps in database
        self.stages = [
            {
                "display_name": "Pre Processing",
                "start": {"regex": "Starting to run step Preproc", "count": 0},
                "end": {"regex": "Starting to run step BoxcarExtract", "count": 0}
            },
            {
                "display_name": "Spectral Extraction",
                "start": {"regex": "Starting to run step BoxcarExtract", "count": 0},
                "end": {"regex": "Starting to run step ApplyFiberFlat_QL", "count": 0}
            },
            {
                "display_name": "Fiber Flattening",
                "start": {"regex": "Starting to run step ApplyFiberFlat_QL", "count": 0},
                "end": {"regex": "Starting to run step SkySub", "count": 0}
            },
            {
                "display_name": "Sky Subtraction",
                "start": {"regex": "Starting to run step SkySub", "count": 0},
                "end": {"regex": "Pipeline completed", "count": 0}
            }
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
                self.resume_log(line, camera.get('name'), lock)
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
 
    def ingest_parallel_qas(self):
        pipe_logger.info('Ingesting QAs...')
        start_ingestion = datetime.datetime.now().replace(microsecond=0)

        proc_qas = list()

        for camera in self.data.get('cameras'):
            output_path = os.path.join(
                desi_spectro_redux,
                self.data.get('output_dir'),
                'ql-*-%s-%s.yaml' % (
                    camera.get('name'),
                    self.data.get('zfill')
                )
            )

            args = (
                camera.get('job_id'),
                camera.get('end'),
                camera.get('status'),
                output_path
            )

            proc = Process(target=self.models.update_job, args=args)
            proc.start()
            proc_qas.append(proc)

        for proc in proc_qas:
            proc.join()

        duration_ingestion = datetime.datetime.now().replace(microsecond=0) - start_ingestion

        pipe_logger.info("(ExpID {}) Ingestion complete: {}.".format(
            self.data.get('expid'), str(duration_ingestion)))
        pipe_logger.info("Total runtime: %s." % (self.data.get('duration') + duration_ingestion))
        pipe_logger.info("ExpID {} is ready for analysis".format(self.data.get('expid')))

    def resume_log(self, line, camera, lock):
        """ """

        lock.acquire()

        try:
            line = line.decode("utf-8").replace('\n', '')
            line_str = line.split(':')[-1]

            if line.find('ERROR') > -1:
                pipe_logger.error("ERROR: Camera {}: {}".format(camera, line_str))
            elif line.find('CRITICAL') > -1:
                pipe_logger.critical("CRITICAL: Camera {}: {}".format(camera, line_str))
            else:
                for stage in self.stages:
                    stage_start = stage.get('start')
                    stage_end = stage.get('end')

                    if line.find(stage_end.get('regex')) > -1:
                        stage_end['count'] += 1

                        if stage_end.get('count') == self.num_cameras:
                            stage_end['time'] = datetime.datetime.now().replace(microsecond=0)
                            pipe_logger.info(
                                '{} ended (runtime: {}).'.format(
                                    stage.get('display_name'),
                                    stage_end.get('time') - stage_start.get('time')
                                )
                            )

                    if line.find(stage_start.get('regex')) > -1:
                        stage_start['count'] += 1

                        if 'time' not in stage_start:
                            stage_start['time'] = datetime.datetime.now().replace(microsecond=0)
                            pipe_logger.info('{} started.'.format(stage.get('display_name')))


        except Exception as err:
            pipe_logger.info(err)

        lock.release()


if __name__ == "__main__":
    print('Standalone execution...')
