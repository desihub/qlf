from qlf_models import QLFModels
from multiprocessing import Process, Event, Value
import datetime
import time
from util import get_config, delete_exposures
from log import get_logger
from qlf_pipeline import QLFProcess
from clients import get_exposure_generator
from threading import Thread
from qlf_configuration import QLFConfiguration

cfg = get_config()

logfile = cfg.get("main", "logfile")
loglevel = cfg.get("main", "loglevel")
allowed_delay = cfg.getfloat("main", "allowed_delay")
generation_limit = 10

logger = get_logger("monitoring", logfile, loglevel)

configuration = QLFConfiguration()


class ExposureMonitoring(Process):

    def __init__(self):
        super().__init__()

        self.process = None
        self.exit = Event()
        self.running = Event()
        self.ics_last_exposure = {}
        self.process_id = Value('i', 0)
        self.generator = get_exposure_generator()

    def run(self):
        """ """
        while not self.exit.is_set():
            time.sleep(1.5)

            if not self.process or not self.process.is_alive():
                self.running.clear()

            exposure = self.generator.last_exposure()

            if not exposure:
                continue

            if exposure.get('expid') == self.ics_last_exposure.get('expid', None):
                continue

            self.ics_last_exposure = exposure

            logger.debug('Exposure ID {} was obtained'.format(exposure.get('expid')))

            # records exposure in database
            QLFModels().insert_exposure(
                exposure.get('expid'),
                exposure.get('night'),
                exposure.get('telra'),
                exposure.get('teldec'),
                exposure.get('tile'),
                exposure.get('dateobs'),
                exposure.get('flavor'),
                exposure.get('exptime')
            )

            if self.process and self.process.is_alive():
                logger.debug('Process ID {} is running.'.format(
                    str(self.process_id.value)
                ))
                continue

            if isinstance(exposure.get('time'), str):
                exposure['time'] = datetime.datetime.strptime(
                    exposure.get('time'), "%Y-%m-%dT%H:%M:%S.%f"
                )

            delay = datetime.datetime.utcnow() - exposure.get('time')
            delay = delay.total_seconds()

            if delay > allowed_delay:
                logger.debug('The delay in the acquisition of the exposure went from {} seconds'.format(
                    str(allowed_delay)
                ))
                continue

            logger.info('Exposure ID {} will be processed.'.format(exposure.get('expid')))

            self.process = Thread(target=process_run, args=(exposure, self.process_id,))
            self.process.start()
            self.running.set()

        delete_exposures()
        logger.info("Bye!")


def process_run(exposure, process_id):
    """ """

    qlf_process = QLFProcess(exposure, configuration.get_current_configuration())
    process_id.value = qlf_process.start_process()
    qlf_process.start_jobs()
    qlf_process.finish_process()


if __name__ == "__main__":
    print('Start Monitoring...')
    monitor = ExposureMonitoring()
    monitor.generator.start()
    monitor.start()
