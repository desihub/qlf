import configparser
import os
import logging
import subprocess
import datetime
import glob
import yaml
from multiprocessing import Process, Manager
from qlf_ingest import QLFIngest


class QLFPipeline(object):
    """ Class responsible for managing Quick Look pipeline execution """

    def __init__(self, data):
        # gets project main directory
        project_path = os.getenv('QLF_ROOT')

        self.cfg = configparser.ConfigParser()
        self.cfg.read('%s/qlf/config/qlf.cfg' % project_path)

        self.pipeline_name = 'Quick Look'

        logname = self.cfg.get("main", "pipeline_log")
        logging.basicConfig(filename=logname, level=logging.DEBUG)
        self.logger = logging.getLogger("%s Pipeline" % self.pipeline_name)

        self.specprod_dir = self.cfg.get('namespace', 'specprod_dir')

        self.register = QLFIngest()

        self.data = data

    def start_process(self):
        """ Start pipeline """

        self.logger.info('starting pipeline ...')
        self.logger.info('night: %s' % self.data.get('night'))
        self.logger.info('exposure: %s' % str(self.data.get('expid')))

        # create process in database to obtain the process_id
        process = self.register.insert_process(
            self.data.get('expid'),
            self.data.get('night'),
            self.pipeline_name
        )

        # TODO: ingest used configuration
        self.register.insert_config(process.id)

        self.logger.info('process ID: %i' % process.id)
        self.logger.info('start: %s' % process.start)
        self.data['start'] = process.start

        output_dir = os.path.join(
            'exposures',
            self.data.get('night'),
            self.data.get('zfill')
        )

        output_full_dir = os.path.join(self.specprod_dir, output_dir)

        if not os.path.isdir(output_full_dir):
            os.makedirs(output_full_dir)

        self.logger.info('output dir: %s' % output_dir)

        self.data['output_dir'] = output_dir

        procs = list()

        return_cameras = Manager().list()

        for camera in self.data.get('cameras'):
            camera['start'] = str(datetime.datetime.now())

            logname = os.path.join(
                self.data.get('output_dir'),
                "run-%s.log" % camera.get('name')
            )

            camera['logname'] = logname

            job = self.register.insert_job(
                process_id=process.id,
                camera=camera.get('name'),
                start=camera.get('start'),
                logname=camera.get('logname')
            )

            camera['job_id'] = job.id

            proc = Process(target=self.execute, args=(camera, return_cameras,))
            procs.append(proc)
            proc.start()

        for proc in procs:
            ret = proc.join()

        self.data['end'] = str(datetime.datetime.now())
        self.logger.info('end: %s' % self.data.get('end'))
        self.logger.info("process completed")

        self.logger.info('begin results ingestion...')

        # TODO: refactor?
        camera_failed = 0

        self.data['cameras'] = return_cameras

        for camera in self.data.get('cameras'):
            self.update_job(camera)

            if not camera.get('status') == 0:
                camera_failed += 1

        status = 0

        if camera_failed > 0:
            status = 1

        process = self.register.update_process(
            process_id=process.id,
            end=self.data.get('end'),
            status=status
        )

        self.logger.info("results ingestion completed")

    def execute(self, camera, return_cameras):
        """ Execute QL Pipeline by camera """

        cmd = (
            'desi_quicklook -n {night} -c {camera} -e {exposure} '
            '-f dark --psfboot {psfboot} --fiberflat {fiberflat} '
            '--rawdata_dir {raw_dir} --specprod_dir {specprod_dir} '
            '--save qlconfig-{camera}-{exposure}'
        ).format(**{
            'night': self.data.get('night'),
            'exposure': str(self.data.get('expid')),
            'camera': camera.get('name'),
            'psfboot': camera.get('psfboot'),
            'fiberflat': camera.get('fiberflat'),
            'raw_dir': self.data.get('raw_dir'),
            'specprod_dir': self.specprod_dir
        })

        self.logger.info(
            "starting job %i with night %s,camera %s and exposure %s... " % (
            camera.get('job_id'),
            self.data.get('night'),
            camera.get('name'),
            self.data.get('expid')
        ))

        logfile = open(os.path.join(
            self.specprod_dir,
            camera.get('logname')
        ), 'wb')

        cwd = os.path.join(
            self.specprod_dir,
            self.data.get('output_dir')
        )

        with subprocess.Popen(cmd, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, shell=True, cwd=cwd) as process:
            logfile.write(process.stdout.read())
            logfile.write(process.stderr.read())
            retcode = process.wait()

        camera['end'] = str(datetime.datetime.now())
        camera['status'] = 0

        if retcode < 0:
            camera['status'] = 1
            msg = (
                "job with camera %s and exposure %s "
                "was terminated by signal: %i "
            ) % (
                camera.get('name'),
                self.data.get('expid'),
                retcode
            )
            self.logger.error(msg)

        return_cameras.append(camera)
        self.logger.info("done job %i" % camera.get('job_id'))

    def update_job(self, camera):
        """ Update job and ingest QA results """

        self.register.update_job(
            job_id=camera.get('job_id'),
            end=camera.get('end'),
            status=camera.get('status')
        )

        output_path = os.path.join(
            self.specprod_dir,
            self.data.get('output_dir'),
            'ql-*-%s-%s.yaml' % (
                camera.get('name'),
                self.data.get('zfill')
            )
        )

        for product in glob.glob(output_path):
            try:
                qa = yaml.load(open(product, 'r'))

                name = os.path.basename(product)
                paname = qa['PANAME']
                metrics = qa['METRICS']

                self.logger.info("registering the product: %s" % name)
                self.register.insert_qa(name, paname, metrics, camera.get('job_id'))
            except Exception as error:
                self.logger.error("error registering product: %s" % product)
                self.logger.error(str(error))

        self.logger.info("product registration has been completed.")

    def was_processed(self):
        """ Returns [<Process object>] if expid was processed else returns [] """

        expid = self.data.get('expid')
        return self.register.get_expid_in_process(expid)


if __name__ == "__main__":
    exposure = {
        'night': '20170428',
        'expid': '3',
        'zfill': '00000003',
        'raw_dir': '/home/singulani/raw_data',
        'cameras': [
          {
            'name': 'r8',
            'psfboot': '/home/singulani/raw_data/20170428/psfboot-r8.fits',
            'fiberflat': '/home/singulani/raw_data/20170428/fiberflat-r8-00000003.fits'
          },
          {
            'name': 'r9',
            'psfboot': '/home/singulani/raw_data/20170428/psfboot-r9.fits',
            'fiberflat': '/home/singulani/raw_data/20170428/fiberflat-r9-00000003.fits'
          }
        ]
    }

    qlp = QLFPipeline(exposure)
    qlp.start_process()
