import datetime
import time
import gc
from multiprocessing import Event, Process, Value
from concurrent import futures
from threading import Thread

from clients import get_exposure_generator, get_qlf_interface
from log import get_logger
from qlf_configuration import QLFConfiguration
from qlf_models import QLFModels
from qlf_pipeline import QLFProcess
from util import get_config

cfg = get_config()

emulate = cfg.getboolean('main', 'emulate_dos')
logfile = cfg.get("main", "logfile")
loglevel = cfg.get("main", "loglevel")
allowed_delay = cfg.getfloat("main", "allowed_delay")

logger = get_logger("monitoring", logfile, loglevel)

configuration = QLFConfiguration()


class ExposureMonitoring(Process):

    def __init__(self):
        super().__init__()

        self.pool = futures.ThreadPoolExecutor(max_workers=1)
        self.process = None

        self.exit = Event()
        self.running = Event()

        self.ics_last_exposure = {}
        self.ics = get_exposure_generator() if emulate else get_qlf_interface()
        self.process_id = Value('i', 0)

    def run(self):
        """ """
        while not self.exit.is_set():
            time.sleep(1.5)

            if not self.process or not self.process.running():
                self.running.clear()

            exposure = self.ics.last_exposure()

            if not exposure:
                logger.debug('No exposure available')
                continue

            ics_last_expid = self.ics_last_exposure.get('exposure_id', None)

            if exposure.get('exposure_id') == ics_last_expid:
                logger.debug('Exposure {} has already been processed'.format(
                    ics_last_expid))
                continue

            self.ics_last_exposure = exposure

            logger.debug('Exposure {} obtained'.format(
                exposure.get('exposure_id')))

            # records exposure in database
            QLFModels().insert_exposure(**exposure)

            if self.process and self.process.running():
                logger.debug('Process {} is running.'.format(
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
                logger.debug((
                    'The delay in the acquisition of the exposure '
                    'went from {} seconds'.format(str(allowed_delay))
                ))
                continue
               
            logger.info('Exposure {} ({} {}) available.'.format(
                exposure.get('exposure_id'),
                exposure.get('program').capitalize(),
                exposure.get('flavor')
            ))

            del self.process
            gc.collect()
            self.process = self.pool.submit(process_run, exposure, self.process_id)

            self.running.set()

        logger.debug("Bye!")

    def shutdown(self):
        """ Turn off monitoring """

        self.exit.set()
        self.running.clear()
        self.pool.shutdown()

        del self.process
        gc.collect()
        self.process = None


def process_run(exposure, process_id):
    """ """

    arms = cfg.get('data', 'arms').split(',')
    spectrographs = cfg.get('data', 'spectrographs').split(',')

    cameras = list()

    for arm in arms:
        for spec in spectrographs:
            cameras.append({'name': arm + spec})

    exposure['cameras'] = cameras

    qlf_process = QLFProcess(
        exposure, configuration.get_current_configuration())
    process_id.value = qlf_process.start_process()
    qlf_process.start_jobs()
    qlf_process.finish_process()


if __name__ == "__main__":
    logger.info('Start Monitoring...')
    monitor = ExposureMonitoring()
    monitor.start()
    monitor.join()
