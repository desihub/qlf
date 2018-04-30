from dos_monitor import DOSmonitor
from qlf_models import QLFModels
from multiprocessing import Process, Event, Value, Manager, Lock
import Pyro4
import configparser
import sys
import os
import errno
from socket import error as socket_error
from log import setup_logger
from procutil import kill_proc_tree
from qlf_pipeline import Jobs as QLFPipeline
from scalar_metrics import LoadMetrics

qlf_root = os.getenv('QLF_ROOT')
cfg = configparser.ConfigParser()

cfg.read('%s/framework/config/qlf.cfg' % qlf_root)
logfile = cfg.get("main", "logfile")
logpipeline = cfg.get("main", "logpipeline")
loglevel = cfg.get("main", "loglevel")

logger = setup_logger("icslogger", logfile, loglevel)
mainlogger = setup_logger("main_logger", "main_daemon.log", loglevel)


class QLFAutoRun(Process):

    def __init__(self, exposures=None):
        super().__init__()
        self.running = Event()
        self.exit = Event()
        self.dos_monitor = DOSmonitor()
        self.process_id = Value('i', 0)
        self.base_night = self.dos_monitor.get_last_night()
        self.list_lock = Lock()
        self.exposures = Manager().list()

        if not exposures:
            exposures = self.dos_monitor.get_exposures_by_night(
                self.base_night)

            for item in exposures:
                item['discovery'] = True
                self.exposures.append(item)
        else:
            self.add_exposures(exposures)

    def add_exposures(self, exposures):
        with self.list_lock:
            for exposure in exposures:
                item = self.dos_monitor.get_exposure(self.base_night, exposure)
                self.exposures.append(item)

    def run(self):
        while not self.get_exit():

            with self.list_lock:
                exposure = self.exposures.pop(0) if self.exposures else None

            if self.get_exit():
                mainlogger.info('Exit is set')
                break

            if not exposure:
                continue

            if exposure.get('discovery', None):
                logger.info('Found expID {}'.format(exposure.get('expid')))

            self.running.set()

            try:
                ql = QLFPipeline(exposure)
                self.process_id.value = ql.start_process()
                ql.start_jobs()
                ql.finish_process()
            except socket_error as serr:
                if serr.errno != errno.ECONNREFUSED:
                    mainlogger.exception('Daemon Error')
                    raise

            self.running.clear()
            self.process_id.value = 0

    def get_current_process_id(self):
        """ """
        return self.process_id.value

    def set_exit(self, value=True):
        """ """
        if value:
            self.exit.set()
        else:
            self.exit.clear()

    def get_exit(self):
        """ """
        return self.exit.is_set()


# TODO: refactor QLFManualRun
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

        for exposure in self.exposures:
            if self.exit.is_set():
                mainlogger.info('Execution stopped')
                break

            self.running.set()
            self.current_exposure = exposure
            ql = QLFPipeline(self.current_exposure)
            mainlogger.info('Executing expid {}...'.format(exposure.get('expid')))
            ql.start_process()
            ql.start_jobs()
            ql.finish_process()

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

    def start(self, exposures=None):
        if self.process and self.process.is_alive():
            self.process.set_exit(False)
            mainlogger.info("Monitor is already initialized (pid: %i)." % self.process.pid)
        else:
            self.process = QLFAutoRun(exposures)
            self.process.start()
            mainlogger.info("Starting pid %i..." % self.process.pid)

    def stop(self):
        if self.process and self.process.is_alive():
            self.process.set_exit()
            mainlogger.info("Stop pid %i" % self.process.pid)

            process_id = self.process.get_current_process_id()
            pid = self.process.pid

            kill_proc_tree(pid, include_parent=False)

            if process_id:
                model = QLFModels()
                model.delete_process(process_id)
        else:
            mainlogger.info("Monitor is not initialized.")

    def reset(self):
        self.stop()

        with open(logfile, 'r+') as ics:
            ics.truncate()

        with open(logpipeline, 'r+') as pipeline:
            pipeline.truncate()

    def add_exposures(self, exposures):

        if not isinstance(exposures, list):
            mainlogger.info("add_exposures function requires a list of exposures")
            return

        if self.process and self.process.is_alive():
            self.process.add_exposures(exposures)
        else:
            self.start(exposures)

    def get_status(self):
        status = False

        if self.process and not self.process.get_exit():
            status = True

        return status

    def is_running(self):
        running = False

        if self.process and self.process.running.is_set():
            running = True

        return running

    def qa_tests(self, process_id):
        qa_tests = list()
        for job in QLFModels().get_jobs_by_process_id(process_id):
            try:
                process = job.process
                exposure = process.exposure
                lm = LoadMetrics(process_id, job.camera_id, process.exposure_id, exposure.night)
                qa_tests.append({job.camera_id: lm.load_qa_tests()})
            except:
                mainlogger.error('qa_tests error camera %s' % job.camera)
        return qa_tests

    def load_scalar_metrics(self, process_id, cam):
        scalar_metrics = dict()
        try:
            process = QLFModels().get_process_by_process_id(process_id)
            exposure = process.exposure
            lm = LoadMetrics(process_id, cam, process.exposure_id, exposure.night)
            scalar_metrics['metrics'] = lm.metrics
            scalar_metrics['tests'] = lm.tests
        except:
            print('load_scalar_metrics error')
        return scalar_metrics

# TODO: refactor QLFManual
@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class QLFManual(object):

    def __init__(self):
        self.process = False
        self.exposures = list()

    def start(self, exposures):
        if self.process and self.process.is_alive():
            self.process.clear()
            mainlogger.info("Monitor is already initialized (pid: %i)." % self.process.pid)
        else:
            self.process = QLFManualRun(exposures)
            self.process.start()
            mainlogger.info("Starting pid %i..." % self.process.pid)

    def stop(self):
        if self.process and self.process.is_alive():
            mainlogger.info("Stop pid %i" % self.process.pid)
            self.process.shutdown()
        else:
            mainlogger.info("Monitor is not initialized.")

    def get_status(self):
        status = False

        if self.process and not self.process.exit.is_set():
            status = True

        mainlogger.info("QLF Manual status: {}".format(status))
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
