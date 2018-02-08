from dos_monitor import DOSmonitor
from qlf_models import QLFModels
from time import sleep
from multiprocessing import Process, Event
import Pyro4
import configparser
import sys
import os
import psutil
import signal
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
        # inicia os eventos running e exit
        self.running = Event()
        self.exit = Event()

        self.dos_monitor = DOSmonitor()

        # TODO
        self.last_night = str()
        self.current_exposure = None
        self.process_id = None

        # pegar a ultima exposure processada no database
        exposure = QLFModels().get_last_exposure()

        if exposure:
            # night do ultimo processamento
            self.last_night = exposure.night

    def run(self):
        # a cada run(start) o evento 'exit' eh limpado
        self.exit.clear()

        # variaveis para controlar messagem de log
        notify_night = False
        notify_exposure = False

        while not self.exit.is_set():

            # pegar a ultima night disponivel no ICS
            night = self.dos_monitor.get_last_night()

            # verifica se ja foi processada
            if night == self.last_night:
                if not notify_night:
                    # Monitoring next night
                    logger.info('Monitoring...')
                    notify_night = True
                sleep(10)
                continue

            notify_night = False

            logger.info('Night {}, waiting for exposures...'.format(night))

            # pega as exposures da night
            exposures = self.dos_monitor.get_exposures_by_night(night)

            if not exposures:
                if not notify_exposure:
                    logger.warn('No exposure was found')
                    notify_exposure = True
                sleep(10)
                continue

            notify_exposure = False

            test = 1

            for exposure in exposures:
                if self.exit.is_set():
                    logger.info('Execution stopped')
                    break

                logger.info('Found expID {}, processing...'.format(exposure.get('expid')))
                self.running.set()
                self.current_exposure = exposure
                sleep(30)
                #ql = QLFPipeline(self.current_exposure)
                #self.process_id = ql.start_process()
                #ql.start_jobs()
                #ql.finish_process()
                self.process_id = test
                logger.info('Process ID {} finished.'.format(self.process_id))
                test += 1
                logger.info('ExpID {} finished.'.format(exposure.get('expid')))

            self.running.clear()
            self.process_id = None
            self.current_exposure = None
            self.last_night = night

        logger.info("Bye!")

    def shutdown(self):
        self.exit.set()
        self.reap_children()
        self.running.clear()
        self.process_id = None
        self.current_exposure = None
        self.last_night = night

    def reap_children(self, timeout=3):
        """Tries hard to terminate and ultimately kill all the children of this process.
        https://psutil.readthedocs.io/en/latest/#terminate-my-children """

        def on_terminate(proc):
            logger.info("process {} terminated with exit code {}".format(proc, proc.returncode))

        procs = psutil.Process().children()
        # send SIGTERM
        for p in procs:
            p.terminate()

        gone, alive = psutil.wait_procs(procs, timeout=timeout, callback=on_terminate)

        if alive:
            # send SIGKILL
            for p in alive:
                logger.info("process {} survived SIGTERM; trying SIGKILL" % p)
                p.kill()

            gone, alive = psutil.wait_procs(alive, timeout=timeout, callback=on_terminate)

            if alive:
                # give up
                for p in alive:
                    logger.info("process {} survived SIGKILL; giving up" % p)

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
            # se tem processo instanciado e ainda esta vivo, a flag 'exit' eh
            # desativada
            self.process.exit.clear()
            logger.info("Monitor is already initialized (pid: %i)." % self.process.pid)
        else:
            # caso contrario a classe de monitoramento de exposures eh
            # instanciada e startada.
            self.process = QLFAutoRun()
            self.process.start()
            logger.info("Starting pid %i..." % self.process.pid)

    def stop(self):
        if self.process and self.process.is_alive():
            # se tem processo instanciado e ainda esta vivo, o processo eh
            # interrompido
            logger.info("Stop pid %i" % self.process.pid)
            process_id = self.process.process_id
            pid = self.process.pid

            if pid == os.getpid():
                raise RuntimeError("I refuse to kill myself")

            parent = psutil.Process(pid)
            children = parent.children(recursive=True)

            children.append(parent)

            for p in children:
                p.send_signal(signal.SIGTERM)

            gone, alive = psutil.wait_procs(children)

            logger.info(gone, alive)

            # self.process.shutdown()

            logger.info('Delete {}?'.format(process_id))
            # verifica se existe algum processo rodando no momento do stop e
            # deleta do database
            if process_id:
                QLFModels().delete_process(process_id)

            # self.process = None
        else:
            logger.info("Monitor is not initialized.")

    def reset(self):
        # interrompe o monitoramento de exposures
        self.stop()
        sleep(5)
        # deleta todo os processos do database
        QLFModels().delete_all_processes()
        # zera o atributo process
        self.process = None

    def get_status(self):
        status = False

        if self.process and not self.process.exit.is_set():
            status = True

        return status

    def get_current_run(self):
        return self.process.current_exposure

    def is_running(self):
        running = False

        if self.process and self.process.running.is_set():
            running = True

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
