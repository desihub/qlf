import os

import Pyro4

from clients import (EXPOSURE_GENERATOR_NS, EXPOSURE_MONITORING_NS, PYRO_HOST,
                     PYRO_PORT, get_exposure_generator)
from exposure_generator import ExposureGenerator
from exposure_monitoring import ExposureMonitoring
from log import get_logger
from procutil import kill_proc_tree
from qlf_configuration import QLFConfiguration
from qlf_models import QLFModels
from scalar_metrics import LoadMetrics
from util import get_config

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

    monitor = False

    # TODO: is provisional while we do not have the ICS.
    exposure_generator = get_exposure_generator()

    def start(self):
        if self.monitor and self.monitor.is_alive():
            self.monitor.exit.clear()
            logger.debug(
                "Monitor is already initialized (pid: {}).".format(
                    self.monitor.pid))
        else:
            self.monitor = ExposureMonitoring()
            self.monitor.start()
            logger.debug("Starting pid %i..." % self.monitor.pid)

        self.exposure_generator.start()

    def stop(self):
        if self.monitor and self.monitor.is_alive():
            self.monitor.exit.set()
            logger.debug("Stop pid %i" % self.monitor.pid)

            pid = self.monitor.pid

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

        if self.monitor and not self.monitor.exit.is_set():
            status = True

        return status

    def is_running(self):
        running = False

        if self.monitor and self.monitor.running.is_set():
            running = True

        return running

    def add_exposures(self, exposures):
        # TODO: improvements
        return None

    def load_scalar_metrics(self, process_id, cam):
        scalar_metrics = dict()
        try:
            process = QLFModels().get_process_by_process_id(process_id)
            exposure = process.exposure
            metrics, tests = LoadMetrics(process_id, cam, process.exposure_id,
                                         exposure.night).Load_metrics_n_tests()
            scalar_metrics['metrics'] = metrics
            scalar_metrics['tests'] = tests
        except Exception as err:
            logger.error(err)
            logger.error('load_scalar_metrics error')
        return scalar_metrics

    def get_current_configuration(self):
        configuration = QLFConfiguration()
        current = configuration.get_current_configuration()
        return current.configuration

    def get_qlconfig(self):
        try:
            config = self.get_current_configuration()
            file = config['qlconfig']
            return file.read()
        except Exception as err:
            logger.info(err)
            return 'Error reading qlconfig'


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class GeneratorControl(object):

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

    # def get_exposure_summary(self, date_range=None, expid_range=None,
    #  require_data_written=True):
    #   # TODO
    #   return

    # def get_exposure_files(self, expid, dest=None,
    # file_class=['desi', 'fibermap'], overwrite=True):
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
            GeneratorControl: exposure_generator
        },
        host=host,
        port=port,
        ns=False
    )


if __name__ == "__main__":
    main()
