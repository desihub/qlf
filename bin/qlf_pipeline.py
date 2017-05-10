import configparser
import os
import logging
import subprocess
import datetime
import pickle
from multiprocessing import Process
from qlf_ingest import QLFIngest


class QLFPipeline(object):
    """ Class responsible for managing pipeline execution """

    def __init__(self, data):
        """ """

        # gets project main directory
        project_path = os.getenv('QLF_PROJECT')

        self.pipeline_name = 'Quick Look'

        self.cfg = configparser.ConfigParser()
        self.cfg.read('%s/config/qlf.cfg' % project_path)

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

        output_dir = os.path.join(
            'exposures',
            self.data.get('night'),
            str(self.data.get('expid')).zfill(8)
        )

        output_full_dir = os.path.join(self.specprod_dir, output_dir)

        if not os.path.isdir(output_full_dir):
            os.makedirs(output_full_dir)

        self.logger.info('output dir: %s' % output_dir)

        self.data['output_dir'] = output_dir

        # create process in database to obtain the process_id
        process = self.register.insert_process(
            self.data.get('expid'),
            self.data.get('night'),
            self.pipeline_name
        )

        self.logger.info('process ID: %i' % process.id)
        self.logger.info('start: %s' % process.start)
        self.data['start'] = process.start

        # TODO: ingest used configuration
        self.register.insert_config(process.id)

        procs = list()

        for camera in self.data.get('cameras'):
            proc = Process(target=self.execute, args=(camera, process.id))
            procs.append(proc)
            proc.start()

        for proc in procs:
            proc.join()

        print(procs)

        self.data['end'] = str(datetime.datetime.now())

        # TODO: calculate status
        status = 1

        process = self.register.update_process(
            process_id=process.id,
            end=self.data.get('end'),
            status=status
        )

        # exp_pckl = '%s.pickle' % self.data.get('expid')
        # full_path_pckl = os.path.join(self.scratchdir, exp_pckl)
        #
        # with open(full_path_pckl, 'wb') as f:
        #     pickle.dump(self.data, f, pickle.HIGHEST_PROTOCOL)
        #
        # self.ingest(full_path_pckl)

        print(self.data)

    def execute(self, camera, process_id):
        """ Execute QL Pipeline """

        camera['start'] = str(datetime.datetime.now())

        logname = os.path.join(
            self.data.get('output_dir'),
            "run-%s.log" % camera.get('name')
        )

        camera['logname'] = logname

        job = self.register.insert_job(
            process_id=process_id,
            camera=camera.get('name'),
            start=camera.get('start'),
            logname=camera.get('logname')
        )

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

        print(cmd)

        logfile = open(os.path.join(self.specprod_dir, logname), 'wb')

        with subprocess.Popen(cmd, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, shell=True) as process:
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

        job = self.register.update_job(
            job_id=job.id,
            end=camera.get('end'),
            status=camera.get('status')
        )

        return retcode

    def ingest(self):
        """ Prepare data to ingest """

        print(self.data)

    def finish(self):
        """ Finish pipeline """
        # TODO
        pass

if __name__ == "__main__":
    exposure = {
        'night': '20170428',
        'expid': 11,
        'raw_dir': '/home/singulani/raw_data/20170428',
        'cameras': [
            {
                'psfboot': '/home/singulani/raw_data/20170428/psfboot-r2.fits',
                'name': 'r2',
                'fiberflat': '/home/singulani/raw_data/20170428/fiberflat-r2-00000011.fits'
            },
            {
                'psfboot': '/home/singulani/raw_data/20170428/psfboot-r3.fits',
                'name': 'r3',
                'fiberflat': '/home/singulani/raw_data/20170428/fiberflat-r3-00000011.fits'
            }
        ]
    }

    qlp = QLFPipeline(exposure)
    qlp.start_process()
