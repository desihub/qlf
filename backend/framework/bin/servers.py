import os
import gc
import Pyro4
from clients import (
    EXPOSURE_MONITORING_NS,
    PYRO_HOST, PYRO_PORT
)
from exposure_monitoring import ExposureMonitoring
from log import get_logger
from procutil import kill_proc_tree
from qlf_models import QLFModels

loglevel = os.environ.get('PIPELINE_LOGLEVEL')
qlf_root = os.environ.get('QLF_ROOT')

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
        if self.is_running():
            QLFModels().abort_current_process()
        if self.monitor and self.monitor.is_alive():
            logger.debug("Stop pid %i" % self.monitor.pid)
            pid = self.monitor.pid
            self.monitor.shutdown()
            kill_proc_tree(pid, include_parent=False)
            del self.monitor
            gc.collect
            self.monitor = None
        else:
            logger.debug("Monitor is not initialized.")

    def reset(self):
        self.stop()

        logfile = os.path.join(qlf_root, "logs", "qlf.log")
        logpipeline = os.path.join(qlf_root, "logs", "pipeline.log")

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

def main():
    exposure_monitoring = EXPOSURE_MONITORING_NS
    host = PYRO_HOST
    port = int(PYRO_PORT)

    Pyro4.Daemon.serveSimple(
        {
            Monitoring: exposure_monitoring,
        },
        host=host,
        port=port,
        ns=False
    )


if __name__ == "__main__":
    main()
