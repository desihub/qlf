from qlf_models import QLFModels
from multiprocessing import Process, Event, Value
import datetime
import time
from util import get_config
from log import get_logger
from qlf_pipeline import QLFProcess
from clients import get_exposure_generator
from threading import Thread
from qlf_configuration import QLFConfiguration

cfg = get_config()

logfile = cfg.get("main", "logfile")
loglevel = cfg.get("main", "loglevel")

logger = get_logger("monitoring", logfile, loglevel)

configuration = QLFConfiguration()


class ExposureMonitoring(Process):

    def __init__(self):
        super().__init__()

        self.processing = None
        self.exit = Event()
        self.allowed_delay = 20.0

        self.generator = get_exposure_generator()

        self.db_last_exposure = QLFModels().get_last_exposure()
        self.ics_last_exposure = {}

        self.process_id = Value('i', 0)

    def run(self):
        """ """
        while not self.exit.is_set():
            time.sleep(1.5)

            exposure = self.generator.last_exposure()

            if not exposure:
                continue

            if exposure.get('expid') == self.ics_last_exposure.get('expid', None):
                continue

            self.ics_last_exposure = exposure

            logger.debug('Exposure ID {} was obtained'.format(exposure.get('expid')))

            # if self.db_last_exposure.exposure_id == int(exposure.get('expid')):
            #     logger.debug('Exposure ID {} has already been ingested.'.format(str(exposure.get('expid'))))
            #     continue

            # records exposure in database
            self.db_last_exposure = QLFModels().insert_exposure(
                exposure.get('expid'),
                exposure.get('night'),
                exposure.get('telra'),
                exposure.get('teldec'),
                exposure.get('tile'),
                exposure.get('dateobs'),
                exposure.get('flavor'),
                exposure.get('exptime')
            )

            if self.processing and self.processing.is_alive():
                logger.debug('Exposure ID {} was not processed as there is active processing.'.format(
                    str(exposure.get('expid'))
                ))
                continue

            if isinstance(exposure.get('time'), str):
                exposure['time'] = datetime.datetime.strptime(
                    exposure.get('time'), "%Y-%m-%dT%H:%M:%S.%f"
                )

            delay = datetime.datetime.utcnow() - exposure.get('time')
            delay = delay.total_seconds()

            if delay > self.allowed_delay:
                logger.debug('The delay in the acquisition of the exposure went from {} seconds'.format(
                    str(self.allowed_delay)
                ))
                continue

            logger.info('Exposure ID {} will be processed.'.format(exposure.get('expid')))

            self.processing = Thread(target=process_run, args=(exposure, self.process_id,))
            self.processing.start()

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
