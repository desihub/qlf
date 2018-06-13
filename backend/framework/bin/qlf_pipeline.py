import glob
import io
import os
import shutil
import subprocess
import time
from datetime import datetime
from multiprocessing import Lock, Manager, Process
from threading import Thread

import matplotlib

from log import get_logger
from qlf_configuration import QLFConfiguration
from qlf_models import QLFModels
from scalar_metrics import LoadMetrics
from util import extract_exposure_data, get_config

matplotlib.use('Agg')

cfg = get_config()

desi_spectro_redux = cfg.get('namespace', 'desi_spectro_redux')
loglevel = cfg.get("main", "loglevel")
logpipeline = cfg.get('main', 'logpipeline')

logger = get_logger("pipeline", logpipeline, loglevel)


class QLFProcess(object):
    """ Class responsible for managing Quick Look pipeline process. """

    def __init__(self, data, configuration):
        self.pipeline_name = 'Quick Look'
        self.data = data

        self.num_cameras = len(self.data.get('cameras'))

        # TODO: improve getting stages
        self.stages = [
            {
                "display_name": "Pre Processing",
                "start": {"regex": "Starting to run step Preproc", "count": 0},
                "end": {"regex": "Starting to run step BoxcarExtract",
                        "count": 0}
            },
            {
                "display_name": "Spectral Extraction",
                "start": {"regex": "Starting to run step BoxcarExtract",
                          "count": 0},
                "end": {"regex": "Starting to run step ApplyFiberFlat_QL",
                        "count": 0}
            },
            {
                "display_name": "Fiber Flattening",
                "start": {"regex": "Starting to run step ApplyFiberFlat_QL",
                          "count": 0},
                "end": {"regex": "Starting to run step SkySub", "count": 0}
            },
            {
                "display_name": "Sky Subtraction",
                "start": {"regex": "Starting to run step SkySub", "count": 0},
                "end": {"regex": "Pipeline completed", "count": 0}
            }
        ]

        self.models = QLFModels()
        self.configuration = configuration

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

        self.data['start'] = datetime.now().replace(microsecond=0)

        # create process in database and obtain the process id
        process = self.models.insert_process(
            self.data,
            self.pipeline_name,
            self.configuration
        )

        self.data['process_id'] = process.id
        self.data['status'] = process.status

        # TODO: ingest configuration file used, this should be done by process
        # self.models.insert_config(process.id)

        logger.info('...\n\n')
        logger.info('Process {}'.format(process.id))
        logger.info('Exposure {} started.'.format(
            self.data.get('exposure_id')
        ))

        return process.id

    def start_jobs(self):
        """ Distributes the cameras for parallel processing. """

        procs = list()
        return_cameras = Manager().list()
        resumelog_lock = Lock()

        for camera in self.data.get('cameras'):
            camera['start'] = datetime.now().replace(microsecond=0)

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

        self.monitor_generated_qa_files = True
        monitor_qa_files = Thread(target=self.monitor_qa_files)
        monitor_qa_files.start()

        for proc in procs:
            proc.join()

        self.monitor_generated_qa_files = False

        self.data['cameras'] = return_cameras

    def start_parallel_job(self, data, camera, return_cameras, lock):
        """ Execute QL Pipeline by camera """

        cmd = [
            'desi_quicklook',
            '-i', data.get('qlconfig'),
            '-n', data.get('night'),
            '-c', camera.get('name'),
            '-e', str(data.get('exposure_id')),
            '--rawdata_dir', data.get('desi_spectro_data'),
            '--specprod_dir', desi_spectro_redux
        ]

        print(" ".join(str(x) for x in cmd))

        # TODO: Add --mergeQA in cmd

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

        camera['end'] = datetime.now().replace(microsecond=0)
        camera['status'] = 0
        camera['duration'] = str(
            camera.get('end') - camera.get('start')
        )

        if retcode < 0:
            camera['status'] = 1

        return_cameras.append(camera)

    def finish_process(self):
        """ Finish pipeline. """

        self.data['end'] = datetime.now().replace(microsecond=0)

        self.data['duration'] = self.data.get('end') - self.data.get('start')

        logger.info("Exposure {} ended ({}).".format(
           self.data.get('exposure_id'),
           str(self.data.get('duration'))
        ))

        proc = Thread(target=self.ingest_parallel_qas)
        proc.start()

    def ingest_parallel_qas(self):
        logger.info('Ingesting QAs...')
        start_ingestion = datetime.now().replace(microsecond=0)

        proc_qas = list()

        for camera in self.data.get('cameras'):
            output_path = os.path.join(
                desi_spectro_redux,
                self.data.get('output_dir'),
                'ql-*-%s-%s.json' % (
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

        qa_tests = self.generate_qa_tests()

        self.models.update_process(
            process_id=self.data.get('process_id'),
            end=self.data.get('end'),
            process_dir=self.data.get('output_dir'),
            status=self.data.get('status'),
            qa_tests=qa_tests
        )

        duration_ingestion = datetime.now().replace(
            microsecond=0) - start_ingestion

        total_duration = self.data.get('duration') + duration_ingestion

        logger.info("Ingestion complete: {}.".format(duration_ingestion))
        logger.info("Total runtime: {}.".format(total_duration))
        logger.info("Exposure {} is ready.".format(
            self.data.get('exposure_id')
        ))

    def generate_qa_tests(self):
        qa_tests = list()
        for camera in self.data.get('cameras'):
            try:
                lm = LoadMetrics(
                    self.data.get('process_id'),
                    camera.get('name'),
                    self.data.get('exposure_id'),
                    self.data.get('night')
                )
                qa_tests.append({camera.get('name'): lm.load_qa_tests()})
            except Exception as err:
                logger.error(err)
                logger.error('qa_tests error camera %s' % camera.get('name'))
        return qa_tests

    def monitor_qa_files(self):
        cameras = dict()
        files = list()
        for camera in self.data.get('cameras'):
            cameras[camera.get('name')] = LoadMetrics(
                None,
                camera.get('name'),
                self.data.get('exposure_id'),
                self.data.get('night')
            )

        while self.monitor_generated_qa_files:
            time.sleep(0.5)
            current_files = glob.glob(os.path.join(
                desi_spectro_redux,
                self.data.get('output_dir'),
                'ql*.json'
            ))

            if len(set(current_files) - set(files)) > 0:
                qa_tests = list()
                for new_file in list(set(current_files) - set(files)):
                    file_array = os.path.basename(new_file).split('-')
                    try:
                        cameras[file_array[2]].update_status(file_array[1])
                    except TypeError as e:
                        current_files = list(
                            set(current_files) - set([new_file])
                        )
                        print("Error {}: {}".format(new_file, e))

                for camera in self.data.get('cameras'):
                    qa_tests.append({
                        camera.get('name'): cameras[camera.get('name')].status
                    })

                if len(qa_tests) > 0:
                    self.models.update_process(
                        process_id=self.data.get('process_id'),
                        end=None,
                        process_dir=self.data.get('output_dir'),
                        status=self.data.get('status'),
                        qa_tests=qa_tests
                    )
                files = current_files

    def resume_log(self, line, camera, lock):
        """ Monitors log per line in camera execution
        and writes to the QL pipeline log.

        Arguments:
            line {str} -- QL execution log file line
            camera {str} -- camera
            lock {object} -- write lock in QL pipeline log
        """

        lock.acquire()

        try:
            line = line.decode("utf-8").replace('\n', '')
            line_str = line.split(':')[-1]

            if line.find('ERROR') > -1 or line.find('CRITICAL') > -1:
                logger.error("ERROR: Camera {}: {}".format(camera, line_str))
            else:
                self.stage_control(line)
        except Exception as err:
            logger.error(err)
        finally:
            lock.release()

    def stage_control(self, line):
        """ Monitors the begin and end of the execution stages of QL per camera.

        Arguments:
            line {str} -- QL execution log file line
        """

        for stage in self.stages:
            stage_start = stage.get('start')
            stage_end = stage.get('end')

            if line.find(stage_end.get('regex')) > -1:
                stage_end['count'] += 1

                if stage_end.get('count') == self.num_cameras:
                    end_time = datetime.now().replace(microsecond=0)
                    stage_end['time'] = end_time
                    logger.info('{} ended ({}).'.format(
                        stage.get('display_name'),
                        stage_end.get('time') - stage_start.get('time')
                    ))

            if line.find(stage_start.get('regex')) > -1:
                stage_start['count'] += 1

                if 'time' not in stage_start:
                    start_time = datetime.now().replace(microsecond=0)
                    stage_start['time'] = start_time
                    logger.info('{} started.'.format(
                        stage.get('display_name')
                    ))


def run_process(exposure_id, night, qlconfig=None, return_process_id=None):
    """ Runs QL pipeline in parallel

    Arguments:
        exposure_id {int} -- exposure ID
        night {str} -- night (YYYYMMDD)

    Keyword Arguments:
        qlconfig {str} -- path to QL config (default: {None})
        return_process_id {object 'multiprocessing.sharedctypes.Value'} --
            process ID object allocated from shared memory.
            (default: {None})

    Returns:
        int -- process ID
    """

    exposure = extract_exposure_data(exposure_id, night)

    arms = cfg.get('data', 'arms').split(',')
    spectrographs = cfg.get('data', 'spectrographs').split(',')

    cameras = list()

    for arm in arms:
        for spec in spectrographs:
            cameras.append({'name': arm + spec})

    exposure['cameras'] = cameras

    configuration = QLFConfiguration()

    if qlconfig:
        exposure['qlconfig'] = qlconfig

    qlf_process = QLFProcess(
        exposure, configuration.get_current_configuration())
    process_id = qlf_process.start_process()

    if return_process_id:
        return_process_id.value = process_id

    qlf_process.start_jobs()
    qlf_process.finish_process()

    return process_id


if __name__ == "__main__":
    print('Manually starting the QL pipeline.')
    import sys

    try:
        exposure_id = int(sys.argv[1])
        night = sys.argv[2]
    except Exception:
        logger.exception('Failed to get exposure ID and night')

    qlconfig = None

    if len(sys.argv) > 3:
        qlconfig = sys.argv[3]

    run_process(exposure_id, night, qlconfig)
