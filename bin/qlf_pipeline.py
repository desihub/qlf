import configparser
import os
import logging
import tempfile
from qlf_ingest import QLFIngest


class QLFPipeline(object):
    """ Class responsible for managing pipeline execution """

    def __init__(self, data):
        """ """

        # gets project main directory
        project_path = os.getenv('QLF_PROJECT')

        self.cfg = configparser.ConfigParser()
        self.cfg.read('%s/config/qlf.cfg' % project_path)

        logname = '/tmp/ql_pipeline.log'
        logging.basicConfig(filename=logname, level=logging.DEBUG)
        self.logger = logging.getLogger("QL Pipeline")

        self.data = data

    def start_process(self):
        """ Start pipeline """

        register = QLFIngest()

        self.logger.info('starting pipeline ...')
        self.logger.info('night: %s' % self.data.get('night'))
        self.logger.info('exposure: %s' % self.data.get('expid'))

        # create process in database to obtain the process_id
        process = register.insert_process(self.data.get('expid'))

        self.logger.info('process ID: %i' % process.id)

        # TODO: ingest used configuration
        register.insert_config(process.id)

        procdir = self.fitdir(process.id)
        scratchdir = self.cfg.get("namespace", "scratch")
        process_dir = os.path.join(scratchdir, procdir)

        self.prepare_process_dir(process_dir)

        self.execute()

    def prepare_process_dir(self, process_dir):
        """ Creates and prepares the process directory with the inputs
        to execute the QL pipeline """

        # create the process_dir
        os.makedirs(process_dir)
        self.logger.info('created process dir: %s' % process_dir)

        self.logger.info('copying input files to process_dir...')

        rawdir = os.path.join(process_dir, 'raw', self.data.get('night'))
        os.makedirs(rawdir)
        self.logger.info('.created directory to raw inputs')

        raw_files = self.data.get('raw_files')
        repo_path = self.data.get('path')

        for raw in raw_files:
            os.system("cp %s %s" % (os.path.join(repo_path, raw), rawdir))
            self.logger.info(".. %s - done." % raw)

        calibdir = os.path.join(process_dir, 'calib', self.data.get('night'))
        os.makedirs(calibdir)
        self.logger.info('.created directory to calib inputs')

        calib_files = [
            self.data.get('psfboot'),
            self.data.get('fiberflat')
        ]

        for calib in calib_files:
            os.system("cp %s %s" % (os.path.join(repo_path, calib), calibdir))
            self.logger.info(".. %s - done." % calib)

    def execute(self):
        """ Execute pipeline """
        # TODO
        pass

    def ingest(self, process_dir):
        """ Prepare data to ingest """
        # TODO
        pass

    def finish(self):
        """ Finish pipeline """
        # TODO
        pass

    def mkconfig(self):
        # TODO: Generate the QL configuration file

        cmd = """
        desi_quicklook --night $NIGHT --flavor "dark" --expid $EXPID --camera
        $CAMERA --rawdata_dir $DESI_SPECTRO_DATA --specprod_dir ./ --fiberflat
        $DESI_CALIB_DATA/fiberflat-r0-00000001.fits --psfboot
        $DESI_CALIB_DATA/psfboot-r0.fits  --save "qlconfig.yaml"
        """
        pass

    def fitdir(self, process_id):
        """ """
        #digit='[0-9]'
        width=8
        #PATTERN=width*digit

        return str(process_id).zfill(width)

if __name__ == "__main__":
    exposure = {
        "night": "20160816",
        "expid": "00000005",
        "camera": "r0",
        "path": "/home/singulani/Projects/desi/test/data/20160816/",
        "raw_files": ["desi-00000005.fits.fz", "fibermap-00000005.fits"],
        "psfboot": "psfboot-r0.fits",
        "fiberflat": "fiberflat-r0-00000001.fits"
    }

    qlp = QLFPipeline(exposure)
    qlp.start_process()
