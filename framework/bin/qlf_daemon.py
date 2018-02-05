from dos_monitor import DOSmonitor
from qlf_models import QLFModels
from time import sleep
from multiprocessing import Process, Event
# import logging
import Pyro4
import configparser
import sys
import os
from log import setup_logger
from qlf_pipeline import Jobs as QLFPipeline

qlf_root = os.getenv('QLF_ROOT')
cfg = configparser.ConfigParser()

try:
    cfg.read('%s/framework/config/qlf.cfg' % qlf_root)
    logfile = cfg.get("main", "logfile")
    loglevel = cfg.get("main", "loglevel")
except Exception as error:
    print(error)
    print("Error reading  %s/framework/config/qlf.cfg" % qlf_root)
    sys.exit(1)

logger = setup_logger("main_logger", logfile, loglevel)


class QLFAutoRun(Process):

    def __init__(self):
        super().__init__()
        self.running = Event()
        self.exit = Event()
        self.dos_monitor = DOSmonitor()
        self.last_night = str()
        self.current_exposure = None

        exposure = QLFModels().get_last_exposure()

        if exposure:
            self.last_night = exposure.night

    def run(self):
        self.clear()
        notify_night = False
        notify_exposure = False

        while not self.exit.is_set():
            night = self.dos_monitor.get_last_night()

            if night == self.last_night:
                if not notify_night:
                    # Monitoring next night
                    logger.info('Monitoring...')
                    notify_night = True
                sleep(10)
                continue

            notify_night = False

            logger.info('Night {}, waiting for exposures...'.format(night))

            exposures = self.dos_monitor.get_exposures_by_night(night)

            if not exposures:
                if not notify_exposure:
                    logger.warn('No exposure was found')
                    notify_exposure = True
                sleep(10)
                continue

            notify_exposure = False

            for exposure in exposures:
                if self.exit.is_set():
                    logger.info('Execution stopped')
                    break

                logger.info('Found expID {}, processing...'.format(exposure.get('expid')))
                self.running.set()
                self.current_exposure = exposure
                ql = QLFPipeline(self.current_exposure)
                ql.start_process()
                ql.start_jobs()
                ql.finish_process()
                logger.info('ExpID {} finished.'.format(exposure.get('expid')))

            self.running.clear()
            self.current_exposure = None
            self.last_night = night

        logger.info("Bye!")

    def clear(self):
        self.exit.clear()

    def shutdown(self):
        self.exit.set()


class QLFManualRun(Process):

    def __init__(self, exposures):
        super().__init__()
        self.running = Event()
        self.exit = Event()
        self.current_exposure = None

        # TODO: improve the method for obtaining exposures
        dos_monitor = DOSmonitor()
        night = dos_monitor.get_last_night()
        self.exposures = list()

        for exposure in exposures:
            self.exposures.append(dos_monitor.get_exposure(night, exposure))

    def run(self):
        self.exit.clear()

        logger.info(self.exposures)

        for exposure in self.exposures:
            logger.info("Initiating {} exposure processing...".format(exposure.get("expid")))

            # if exit is set
            if self.exit.is_set():
                logger.info('Execution stopped')
                break

            # is running
            self.running.set()
            self.current_exposure = exposure
            ql = QLFPipeline(self.current_exposure)
            logger.info('Executing expid {}...'.format(exposure.get('expid')))
            ql.start_process()
            ql.start_jobs()
            ql.finish_process()

        # not running
        self.running.clear()
        self.current_exposure = None

        logger.info("Bye!")
        self.shutdown()

    def clear(self):
        self.exit.clear()

    def shutdown(self):
        self.exit.set()


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class QLFAutomatic(object):
    def __init__(self):
        self.process = False

    def start(self):
        if self.process and self.process.is_alive():
            self.process.clear()
            logger.info("Monitor is already initialized (pid: %i)." % self.process.pid)
        else:
            self.process = QLFAutoRun()
            self.process.start()
            logger.info("Starting pid %i..." % self.process.pid)

    def stop(self):
        if self.process and self.process.is_alive():
            logger.info("Stop pid %i" % self.process.pid)
            self.process.shutdown()
        else:
            logger.info("Monitor is not initialized.")

    def restart(self):
        self.stop()
        logger.info("Restarting...")
        sleep(5)
        self.start()

    def get_status(self):
        status = False

        if self.process and not self.process.exit.is_set():
            status = True

        # logger.info("QLF Daemon status: {}".format(status))
        return status

    def get_current_run(self):
        return self.process.current_exposure

    def is_running(self):
        running = False

        if self.process and self.process.running.is_set():
            running = True

        # logger.info("Running? {}".format(running))
        return running


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class QLFManual(object):

    def __init__(self):
        self.process = False
        self.exposures = list()

    def start(self, exposures):
        if self.process and self.process.is_alive():
            self.process.clear()
            logger.info("Monitor is already initialized (pid: %i)." % self.process.pid)
        else:
            self.process = QLFManualRun(exposures)
            self.process.start()
            logger.info("Starting pid %i..." % self.process.pid)

    def stop(self):
        if self.process and self.process.is_alive():
            logger.info("Stop pid %i" % self.process.pid)
            self.process.shutdown()
        else:
            logger.info("Monitor is not initialized.")

    def get_status(self):
        status = False

        if self.process and not self.process.exit.is_set():
            status = True

        logger.info("QLF Manual status: {}".format(status))
        return status

    def get_current_run(self):
        return self.process.current_exposure


def main():
    try:
        auto_mode = os.environ.get('QLF_DAEMON_NS', 'qlf.daemon')
        manual_mode = os.environ.get('QLF_MANUAL_NS', 'qlf.manual')
        host = os.environ.get('QLF_DAEMON_HOST', 'localhost')
        port = int(os.environ.get('QLF_DAEMON_PORT', '56005'))
    except Exception as err:
        logger.error(err)
        sys.exit(1)

    Pyro4.Daemon.serveSimple(
        {QLFAutomatic: auto_mode, QLFManual: manual_mode},
        host=host,
        port=port,
        ns=False
    )


if __name__ == "__main__":
    main()
