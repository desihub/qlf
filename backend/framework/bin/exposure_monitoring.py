import datetime
import time
import gc
from multiprocessing import Event, Process, Value
from concurrent import futures
from threading import Thread
import os
import errno
from socket import error as socket_error

from clients import get_qlf_interface
from log import get_logger
from qlf_models import QLFModels
from qlf_pipeline import run_process

allowed_delay = float(os.environ.get("PIPELINE_DELAY"))
qlf_root = os.environ.get('QLF_ROOT')

logger = get_logger(
    'qlf.monitoring',
    os.path.join(qlf_root, "logs", "monitoring.log")
)

pipe_logger = get_logger(
    'qlf.pipeline',
    os.path.join(qlf_root, "logs", "pipeline.log")
)

daemon_logger = get_logger(
    'qlf.daemon',
    os.path.join(qlf_root, "logs", "qlf_daemon.log")
)

class ExposureMonitoring(Process):

    def __init__(self):
        super().__init__()

        self.pool = futures.ThreadPoolExecutor(max_workers=1)
        self.process = None

        self.exit = Event()
        self.running = Event()

        self.ics_last_exposure = {}
        self.ics = get_qlf_interface()
        self.process_id = Value('i', 0)

    def run(self):
        """ """
        while not self.exit.is_set():
            time.sleep(1.5)

            if not self.process or not self.process.running():
                self.running.clear()

            last_exposure = self.ics.last_exposure()
            try:
                exposure = last_exposure['exposure']
                fibermap = last_exposure['fibermap']
            except:
                logger.debug('No exposure available')
                continue

            fibermap = last_exposure.get('fibermap', None)

            ics_last_expid = self.ics_last_exposure.get('exposure_id', None)

            if exposure.get('exposure_id') == ics_last_expid:
                logger.debug('Exposure {} has already been processed'.format(
                    ics_last_expid))
                continue

            self.ics_last_exposure = exposure

            logger.debug('Exposure {} obtained'.format(
                exposure.get('exposure_id')))

            # records exposure in database
            exposure_obj = QLFModels().insert_exposure(**exposure)
            if exposure_obj:
                fibermap['exposure'] = exposure_obj
                QLFModels().insert_fibermap(**fibermap)

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
            self.process = self.pool.submit(run_process, exposure, self.process_id)
            self.process.add_done_callback(future_callback)

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


def future_callback(process):
    """ Catch pipeline processing return.
    
    Arguments:
        process {concurrent.futures object} -- background process
    """

    try:
        process.result()
    except socket_error as serr:
        if serr.errno != errno.ECONNREFUSED:
            pipe_logger.exception("Error in communicating with QL pipeline executor.")
        
        daemon_logger.exception('QL pipeline: stopped processing.')
    except Exception:
        daemon_logger.exception('QL pipeline error.')


if __name__ == "__main__":
    logger.info('Start Monitoring...')
    monitor = ExposureMonitoring()
    monitor.start()
    monitor.join()