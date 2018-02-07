from time import sleep
from multiprocessing import Process, Event
import Pyro4
import sys
import os
import psutil
import signal
from log import setup_logger
from procutil import *

logfile = 'test.log'

logger = setup_logger("main_logger", logfile)


class QLFAutoRun(Process):

    def __init__(self):
        super().__init__()
        # inicia os eventos running e exit
        self.running = Event()
        self.exit = Event()

        self.id = None

    def run(self):
        # a cada run(start) o evento 'exit' eh limpado
        self.exit.clear()

        count = 0

        while not self.exit.is_set():
            count += 1
            logger.info('Found expID {}, processing...'.format(count))
            self.running.set()
            sleep(30)
            self.id = count
            logger.info('ExpID {} finished.'.format(count))

        self.running.clear()
        self.id = None
        logger.info("Bye!")

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

            kill_proc_tree(pid)
            # self.process.shutdown()

            logger.info('Delete {}?'.format(process_id))
        else:
            logger.info("Monitor is not initialized.")

    def reset(self):
        # interrompe o monitoramento de exposures
        self.stop()
        sleep(5)
        # deleta todo os processos do database
        logger.info('Delete ALL?')

        # zera o atributo process
        self.process = None

    def get_status(self):
        status = False

        if self.process and not self.process.exit.is_set():
            status = True

        return status


def main():
    try:
        auto_mode = os.environ.get('QLF_DAEMON_NS', 'qlf.daemon')
        host = os.environ.get('QLF_DAEMON_HOST', 'localhost')
        port = int(os.environ.get('QLF_DAEMON_PORT', '56005'))
    except Exception as err:
        logger.error(err)
        sys.exit(1)

    Pyro4.Daemon.serveSimple(
        {QLFAutomatic: auto_mode},
        host=host,
        port=port,
        ns=False
    )


if __name__ == "__main__":
    main()
