import os
import gc
import Pyro4
from clients import (
    EXPOSURE_GENERATOR_NS, EXPOSURE_MONITORING_NS,
    PYRO_HOST, PYRO_PORT
)
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
emulate = cfg.getboolean("main", "emulate_dos")
qlf_root = cfg.get("environment", "qlf_root")
base_exposures_path = cfg.get("namespace", "base_exposures_path")

logger = get_logger(
    "pyro.servers",
    os.path.join(qlf_root, "logs", "servers.log"),
    loglevel
)


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Monitoring(object):

    monitor = False

    def start(self):
        if self.monitor and self.monitor.is_alive():
            logger.debug(
                "Monitor is already initialized (pid: {}).".format(
                    self.monitor.pid))
        else:
            self.monitor = ExposureMonitoring()
            self.monitor.start()
            logger.debug("Starting pid %i..." % self.monitor.pid)

    def stop(self):
        if self.monitor and self.monitor.is_alive():
            logger.debug("Stop pid %i" % self.monitor.pid)
            pid = self.monitor.pid
            self.monitor.shutdown()
            kill_proc_tree(pid, include_parent=False)
            QLFModels().abort_current_process()
            del self.monitor
            gc.collect
            self.monitor = None
        else:
            logger.debug("Monitor is not initialized.")

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

    def get_default_configuration(self):
        configuration = QLFConfiguration()
        default = configuration.get_default_configuration()
        return default

    def get_calibration(self):
        return os.listdir(os.path.join(base_exposures_path, 'psf'))


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
        if self.generator:
            try:
                last = dict(self.generator.get_last_exposure())
            except Exception as err:
                logger.error(err)
                last = dict()
        else:
            logger.debug("Exposure generator is not initialized.")
            last = dict()

        return last


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
