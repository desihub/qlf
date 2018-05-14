from exposure_monitoring import ExposureMonitoring
from exposure_generator import ExposureGenerator

import Pyro4
import os

from log import get_logger
from procutil import kill_proc_tree
from util import get_config
from scalar_metrics import LoadMetrics
from qlf_models import QLFModels

from clients import EXPOSURE_MONITORING_NS, EXPOSURE_GENERATOR_NS, PYRO_HOST, PYRO_PORT
from clients import get_exposure_generator

cfg = get_config()
loglevel = cfg.get("main", "loglevel")
qlf_root = cfg.get("environment", "qlf_root")

logger = get_logger(
    "pyro.servers",
    os.path.join(qlf_root, "logs", "servers.log"),
    loglevel
)


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Monitoring(object):

    monitoring = False

    # TODO: is provisional while we do not have the ICS.
    exposure_generator = get_exposure_generator()

    def start(self):
        if self.monitoring and self.monitoring.is_alive():
            self.monitoring.exit.clear()
            logger.debug("Monitor is already initialized (pid: %i)." % self.monitoring.pid)
        else:
            self.monitoring = ExposureMonitoring()
            self.monitoring.start()
            logger.debug("Starting pid %i..." % self.monitoring.pid)

        self.exposure_generator.start()

    def stop(self):
        if self.monitoring and self.monitoring.is_alive():
            self.monitoring.exit.set()
            logger.debug("Stop pid %i" % self.monitoring.pid)

            pid = self.monitoring.pid

            kill_proc_tree(pid, include_parent=False)
        else:
            logger.debug("Monitor is not initialized.")

        self.exposure_generator.stop()

    def reset(self):
        self.stop()

        logfile = cfg.get("main", "logfile")
        logpipeline = cfg.get('main', 'logpipeline')

        for log in [logfile, logpipeline]:
            with open(log, 'r+') as filelog:
                filelog.truncate()

    def get_status(self):
        status = False

        if self.monitoring and not self.monitoring.exit.is_set():
            status = True

        return status

    def is_running(self):
        running = False

        if self.monitoring and self.monitoring.running.is_set():
            running = True

        return running

    def add_exposures(self, exposures):
        # TODO: improvements
        return None

    def qa_tests(self, process_id):
        qa_tests = list()
        for job in QLFModels().get_jobs_by_process_id(process_id):
            try:
                process = job.process
                exposure = process.exposure
                lm = LoadMetrics(process_id, job.camera_id, process.exposure_id, exposure.night)
                qa_tests.append({job.camera_id: lm.load_qa_tests()})
            except Exception as err:
                logger.error(err)
                logger.error('qa_tests error camera %s' % job.camera)
        return qa_tests

    def load_scalar_metrics(self, process_id, cam):
        scalar_metrics = dict()
        try:
            process = QLFModels().get_process_by_process_id(process_id)
            exposure = process.exposure
            lm = LoadMetrics(process_id, cam, process.exposure_id, exposure.night)
            scalar_metrics['metrics'] = lm.metrics
            scalar_metrics['tests'] = lm.tests
        except Exception as err:
            logger.error(err)
            logger.error('load_scalar_metrics error')
        return scalar_metrics


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Generator(object):

    generator = False

    def start(self):
        if self.generator and self.generator.is_alive():
            logger.debug("Exposure generator is already initialized.")
        else:
            self.generator = ExposureGenerator()
            self.generator.start()

    def stop(self):
        logger.debug(self.generator)
        if self.generator and self.generator.is_alive():
            logger.debug("Stop pid %i" % self.generator.pid)
            self.generator.terminate()
        else:
            logger.debug("Exposure generator is not initialized.")

    def last_exposure(self):
        if self.generator and self.generator.is_alive():
            return dict(self.generator.get_last_exposure())
        else:
            logger.debug("Exposure generator is not initialized.")
            return dict()

    # def get_exposure_summary(self, date_range=None, expid_range=None, require_data_written=True):
    #   # TODO
    #   return
    #
    # def get_exposure_files(self, expid, dest=None, file_class=['desi', 'fibermap'], overwrite=True):
    #   # TODO
    #   return


def main():

    exposure_monitoring = EXPOSURE_MONITORING_NS
    exposure_generator = EXPOSURE_GENERATOR_NS
    host = PYRO_HOST
    port = int(PYRO_PORT)

    Pyro4.Daemon.serveSimple(
        {
            Monitoring: exposure_monitoring,
            Generator: exposure_generator
        },
        host=host,
        port=port,
        ns=False
    )


if __name__ == "__main__":
    main()
