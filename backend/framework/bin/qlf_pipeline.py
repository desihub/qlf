import glob
import io
import os
import gc
import shutil
import subprocess
import time
import json
from datetime import datetime
from multiprocessing import Lock, Manager, Process
from threading import Thread
from concurrent import futures
from util import check_hdu

import logging

from qlf_models import QLFModels
from scalar_metrics import LoadMetrics

desi_spectro_redux = os.environ.get('DESI_SPECTRO_REDUX')
max_workers = int(os.environ.get('PIPELINE_MAX_WORKERS'))
qlf_root = os.environ.get('QLF_ROOT')

logger = logging.getLogger(name='qlf.pipeline')

if not max_workers > 0:
    max_workers = None


class QLFProcess(object):
    """ Class responsible for managing Quick Look pipeline process. """

    def __init__(self, data):
        self.pipeline_name = 'Quick Look'
        self.data = data

        self.num_cameras = len(self.data.get('cameras'))

        flavor_path = os.path.join(
            qlf_root, "framework", "ql_mapping",
            "{}.json".format(self.data.get('flavor'))
        )

        with open(flavor_path) as f:
            flavor = json.load(f)

        self.stages = flavor.get('step_list')

        for stage in self.stages:
            stage['start'] = {"regex": stage.get('start'), "count": 0}
            stage['end'] = {"regex": stage.get('end'), "count": 0}

        self.models = QLFModels()

        output_dir = os.path.join(
            'exposures',
            self.data.get('night'),
            self.data.get('zfill')
        )

        output_full_dir = os.path.join(desi_spectro_redux, output_dir)

        if not os.path.isdir(output_full_dir):
            os.makedirs(output_full_dir)

        self.data['output_dir'] = output_dir

    def start_process(self):
        """ Start pipeline. """

        self.data['start'] = datetime.now().replace(microsecond=0)

        # create process in database and obtain the process id
        process = self.models.insert_process(
            self.data,
            self.pipeline_name
        )

        self.data['process_id'] = process.id
        self.data['status'] = process.status

        logger.info('...\n\n')
        logger.info('Process {}'.format(process.id))
        logger.info('Exposure {} started.'.format(
            self.data.get('exposure_id')
        ))

        process_dir = os.path.join(
            self.data.get('output_dir'),
            str(process.id).zfill(8)
        )

        if not os.path.isdir(os.path.join(
            desi_spectro_redux, process_dir
        )):
            os.makedirs(os.path.join(
                desi_spectro_redux, process_dir
            ))

        self.data['process_dir'] = process_dir

        return process.id

    def start_jobs(self):
        """ Distributes the cameras for parallel processing. """

        procs = list()
        return_cameras = Manager().list()
        resumelog_lock = Lock()

        pool = futures.ThreadPoolExecutor(max_workers=max_workers)

        for camera in self.data.get('cameras'):
            camera['start'] = datetime.now().replace(microsecond=0)

            logname = os.path.join(
                self.data.get('process_dir'),
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

            procs.append(pool.submit(
                self.start_parallel_job,
                self.data,
                camera,
                return_cameras,
                resumelog_lock,
            ))

        for proc in futures.as_completed(procs):
            proc.result()

        procs.clear()
        gc.collect()

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
            '--specprod_dir', desi_spectro_redux,
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
                self.data.get('output_dir')
            )

            args = (
                camera.get('job_id'),
                self.data.get('exposure_id'),
                camera.get('name'),
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

        if "ALARM" in str(qa_tests):
            self.data['status'] = 1

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
                    self.data.get('night'),
                    self.data.get('flavor')
                )
                lm.get_merged_qa_status()
                qa_tests.append({
                    camera.get('name'): lm.qas_status
                })
            except Exception as err:
                logger.error(err)
                logger.error('qa_tests error camera %s' % camera.get('name'))
        return qa_tests

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
                self.num_cameras = self.num_cameras - 1
            if line.find('File does not exist') > -1:
                logger.error("ERROR: Camera {}: {}".format(camera, line))
                self.num_cameras = self.num_cameras - 1
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


def run_process(exposure, return_process_id=None):
    """ Runs QL pipeline in parallel

    Arguments:
        exposure {dict} -- exposure info 
        e.g. of keys expected: exposure_id, dateobs, night, zfill,
        desi_spectro_data, desi_spectro_redux, telra, teldec, tile,
        flavor, program, airmass, exptime, qlconfig, time

        The util.extract_exposure_data function returns this dictionary
        or can be created by database if the exposition has already been
        processed.

    Keyword Arguments:
        return_process_id {object 'multiprocessing.sharedctypes.Value'} --
            process ID object allocated from shared memory.
            (default: {None})

    Returns:
        int -- process ID
    """

    arms = os.environ.get('PIPELINE_ARMS').split(',')
    spectrographs = os.environ.get('PIPELINE_SPECTROGRAPHS').split(',')

    cameras = list()
    available_cameras = check_hdu(exposure['exposure_id'], exposure['night'])

    for arm in arms:
        for spec in spectrographs:
            if arm + spec in available_cameras:
                cameras.append({'name': arm + spec})
            else:
                logger.info('{} not found in header'.format(arm + spec))

    exposure['cameras'] = cameras

    qlf_process = QLFProcess(exposure)
    process_id = qlf_process.start_process()

    if return_process_id:
        return_process_id.value = process_id

    qlf_process.start_jobs()
    qlf_process.finish_process()

    return process_id


if __name__ == "__main__":
    import sys
    from util import extract_exposure_data

    logger.info('Manually starting the QL pipeline.')

    try:
        exposure_id = int(sys.argv[1])
        night = sys.argv[2]
    except Exception:
        logger.exception('Failed to get exposure ID and night')

    exposure = extract_exposure_data(exposure_id, night)

    run_process(exposure)
