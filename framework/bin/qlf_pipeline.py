import os
import io
import logging
import subprocess
import datetime
from multiprocessing import Manager
from threading import Thread
from qlf_models import QLFModels
from celery import group
from tasks import start_parallel_job

logger = logging.getLogger(__name__)


class QLFProcess(object):
    """ Class responsible for managing Quick Look pipeline process. """

    def __init__(self, data):
        self.pipeline_name = 'Quick Look'
        self.data = data
        self.models = QLFModels()

    def start_process(self):
        """ Start pipeline. """

        logger.info('Started %s ...' % self.pipeline_name)
        logger.info('Night: %s' % self.data.get('night'))
        logger.info('Exposure: %s' % str(self.data.get('expid')))

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

        logger.info('Process ID: %i' % process.id)
        logger.info('Starting...')

        output_dir = os.path.join(
            'exposures',
            self.data.get('night'),
            self.data.get('zfill')
        )

        output_full_dir = os.path.join(self.data.get('desi_spectro_redux'), output_dir)

        # Make sure output dir is created
        if not os.path.isdir(output_full_dir):
            os.makedirs(output_full_dir)

        logger.info('Output dir: %s' % output_dir)

        self.data['output_dir'] = output_dir

    def finish_process(self):
        """ Finish pipeline. """

        self.data['end'] = datetime.datetime.now().replace(microsecond=0)

        self.data['duration'] = str(self.data.get('end') - self.data.get('start'))

        logger.info("Process with expID {} completed in {}.".format(
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
        self.job_runs = None

    def start_jobs(self):
        """ Distributes the cameras for parallel processing. """

        return_cameras = Manager().list()
        runs = list()

        for camera in self.data.get('cameras'):
            camera['start'] = datetime.datetime.now().replace(
                microsecond=0
            )

            logname = os.path.join(
                self.data.get('output_dir'),
                "run-%s.log" % camera.get('name')
            )

            camera['logname'] = logname

            logger.info('Output log for camera %s: %s' % (
                camera.get('name'), camera.get('logname')
            ))

            job = self.models.insert_job(
                process_id=self.data.get('process_id'),
                camera=camera.get('name'),
                start=camera.get('start'),
                logname=camera.get('logname')
            )

            camera['job_id'] = job.id

            runs.append(start_parallel_job.s(self.data, camera))

            # args = (
            #     self.data,
            #     camera,
            #     return_cameras,
            # )

        jobs = group(runs)
        self.job_runs = jobs.apply_async()
        # self.job_runs.join()

        #     proc = Thread(target=self.start_parallel_job, args=args)
        #     proc.start()
        #     procs.append(proc)
        #
        # for proc in procs:
        #     proc.join()

        # self.data['cameras'] = return_cameras
        #
        # logger.info('Begin ingestion of results...')
        # start_ingestion = datetime.datetime.now().replace(microsecond=0)
        #
        # # TODO: refactor?
        # camera_failed = 0
        #
        # for camera in self.data.get('cameras'):
        #     output_path = os.path.join(
        #         self.data.get('desi_spectro_redux'),
        #         self.data.get('output_dir'),
        #         'ql-*-%s-%s.yaml' % (
        #             camera.get('name'),
        #             self.data.get('zfill')
        #         )
        #     )
        #
        #     self.models.update_job(
        #         job_id=camera.get('job_id'),
        #         end=camera.get('end'),
        #         status=camera.get('status'),
        #         output_path=output_path
        #     )
        #
        #     if not camera.get('status') == 0:
        #         camera_failed += 1
        #
        # status = 0
        #
        # if camera_failed > 0:
        #     status = 1
        #
        # self.data['status'] = status
        #
        # duration_ingestion = str(
        #     datetime.datetime.now().replace(microsecond=0) - start_ingestion
        # )
        #
        # logger.info("Results ingestion complete in %s." % duration_ingestion)

    # @staticmethod
    # def start_parallel_job(data, camera, return_cameras):
    #     """ Execute QL Pipeline by camera """
    #
    #     cmd = [
    #         'desi_quicklook',
    #         '-i', data.get('qlconfig'),
    #         '-n', data.get('night'),
    #         '-c', camera.get('name'),
    #         '-e', str(data.get('expid')),
    #         '--rawdata_dir', data.get('desi_spectro_data'),
    #         '--mergeQA',
    #         '--specprod_dir', data.get('desi_spectro_redux')
    #     ]
    #
    #     logger.info(
    #         "Started job %i on exposure %s and camera %s ... " % (
    #         camera.get('job_id'),
    #         data.get('expid'),
    #         camera.get('name')
    #     ))
    #
    #     logname = io.open(os.path.join(
    #         data.get('desi_spectro_redux'),
    #         camera.get('logname')
    #     ), 'wb')
    #
    #     cwd = os.path.join(
    #         data.get('desi_spectro_redux'),
    #         data.get('output_dir')
    #     )
    #
    #     with subprocess.Popen(cmd, stdout=logname,
    #                           stderr=subprocess.STDOUT, cwd=cwd) as process:
    #         while process.poll() is None:
    #             logname.flush()
    #
    #         retcode = process.wait()
    #
    #     camera['end'] = datetime.datetime.now().replace(microsecond=0)
    #     camera['status'] = 0
    #     camera['duration'] = str(
    #         camera.get('end') - camera.get('start')
    #     )
    #
    #     if retcode < 0:
    #         camera['status'] = 1
    #         msg = (
    #             "Job on exposure %s and camera %s "
    #             "finished with code %i in %s"
    #         ) % (
    #             camera.get('name'),
    #             data.get('expid'),
    #             retcode,
    #             camera.get('duration')
    #         )
    #         logger.error(msg)
    #
    #     return_cameras.append(camera)
    #
    #     logger.info("Finished job %i in %s" % (
    #         camera.get('job_id'),
    #         camera.get('duration')
    #     ))


if __name__ == "__main__":
    print('Standalone execution...')
