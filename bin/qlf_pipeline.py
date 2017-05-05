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
        self.scratchdir = self.cfg.get("namespace", "scratch")

        logname = '/tmp/ql_pipeline.log'
        logging.basicConfig(filename=logname, level=logging.DEBUG)
        self.logger = logging.getLogger("%s Pipeline" % self.pipeline_name)

        self.data = data

    def start_process(self):
        """ Start pipeline """

        register = QLFIngest()

        self.logger.info('starting pipeline ...')
        self.logger.info('night: %s' % self.data.get('night'))
        self.logger.info('exposure: %s' % self.data.get('expid'))

        # create process in database to obtain the process_id
        process = register.insert_process(
            self.data.get('expid'),
            self.data.get('night'),
            self.pipeline_name
        )

        self.logger.info('process ID: %i' % process.id)
        self.logger.info('start: %s' % process.start)
        self.data['start'] = process.start

        # TODO: ingest used configuration
        register.insert_config(process.id)

        procdir = self.fitdir(process.id)
        self.data['process_dir'] = procdir

        full_process_dir = os.path.join(self.scratchdir, procdir)

        os.makedirs(full_process_dir)
        self.logger.info('created process dir: %s' % full_process_dir)

        procs = list()

        for ccd in self.data.get('ccds'):
            camera_dir = os.path.join(
                full_process_dir,
                ccd.get("camera")
            )

            if not os.path.isdir(camera_dir):
                os.makedirs(camera_dir)
                self.logger.info('created camera dir')

            self.mkconfig(camera_dir, ccd)

            ccd['camera_dir'] = camera_dir

            self.logger.info('camera dir: %s' % camera_dir)

            proc = Process(target=self.execute, args=(ccd,))
            procs.append(proc)
            proc.start()

        for proc in procs:
            proc.join()

        print(procs)

        self.data['end'] = str(datetime.datetime.now())

        exp_pckl = '%s.pickle' % self.data.get('expid')
        full_path_pckl = os.path.join(self.scratchdir, exp_pckl)

        with open(full_path_pckl, 'wb') as f:
            pickle.dump(self.data, f, pickle.HIGHEST_PROTOCOL)

        self.ingest(full_path_pckl)

    def execute(self, ccd):
        """ Execute QL Pipeline  """

        ccd['start'] = str(datetime.datetime.now())

        camera_dir = ccd.get('camera_dir')
        config_file = ccd.get('config')

        ccd['name'] = config_file

        self.logger.info('executing: %s' % config_file)

        path_config = os.path.join(camera_dir, config_file)

        if not os.path.isfile(path_config):
            raise OSError(2, 'Config not found', path_config)

        pipeline_setup = self.cfg.get('main', 'pipeline_setup')
        conda_env = self.cfg.get('main', 'conda_env')

        cmd = (
            'env -i HOME=$HOME TERM=$TERM bash -c " '
            'source %s desi && '
            '. %s && '
            'cd %s && '
            'desi_quicklook -c %s"'
        ) % (conda_env, pipeline_setup, camera_dir, config_file)

        print(cmd)

        logname = os.path.join(
            self.data.get('process_dir'),
            ccd.get('camera'),
            "%s-%s.log" % (ccd.get('camera'), self.data.get('expid'))
        )

        ccd['logname'] = logname
        logfile = open(os.path.join(self.scratchdir, logname), 'wb')

        with subprocess.Popen(cmd, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, shell=True) as process:
            logfile.write(process.stdout.read())
            logfile.write(process.stderr.read())
            retcode = process.wait()

        ccd['end'] = str(datetime.datetime.now())

        return retcode

    def ingest(self, pickle_data):
        """ Prepare data to ingest """

        print(pickle_data)
        print(self.data)


    def finish(self):
        """ Finish pipeline """
        # TODO
        pass

    def mkconfig(self, camera_dir, ccd):
        # TODO: Generate the QL configuration file

        print(ccd)

        config_original_path = os.path.join(
            self.data.get("path"),
            ccd.get("config")
        )

        config_path = os.path.join(camera_dir, ccd.get("config"))

        self.logger.info('copying config file to camera_dir...')
        os.system("cp %s %s" % (
            config_original_path,
            config_path
        ))

        cmd = """
        desi_quicklook --night $NIGHT --flavor "dark" --expid $EXPID --camera
        $CAMERA --rawdata_dir $DESI_SPECTRO_DATA --specprod_dir ./ --fiberflat
        $DESI_CALIB_DATA/fiberflat-r0-00000001.fits --psfboot
        $DESI_CALIB_DATA/psfboot-r0.fits  --save "qlconfig.yaml"
        """

    def fitdir(self, process_id):
        """ """
        return str(process_id).zfill(8)

if __name__ == "__main__":
    exposure = {
        "night": "20160816",
        "expid": "00000010",
        "path": "/home/singulani/Projects/desi/test/data/20160816/",
        "ccds": [
            {
                "camera": "r0",
                "raw_files": ["desi-00000010.fits.fz", "fibermap-00000010.fits"],
                "psfboot": "psfboot-r0.fits",
                "fiberflat": "fiberflat-r0-00000001.fits",
                "config": "config-r0-00000010.yaml"
            }
        ]
    }

    qlp = QLFPipeline(exposure)
    qlp.start_process()
    #qlp.execute("/home/singulani/Projects/desi/scratch/00000000")

