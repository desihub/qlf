from time import sleep
from multiprocessing import Process, Event, Value
import Pyro4
import sys
import os
from log import setup_logger
import subprocess
from procutil import kill_proc_tree

logfile = 'test.log'

logger = setup_logger("main_logger", logfile)


class QLFAutoRun(Process):

    def __init__(self):
        super().__init__()

        # inicia os eventos running e exit
        self.running = Event()
        self.exit = Event()

        self.id = Value('i', 0)

    def run(self):
        count = 1

        while not self.exit.is_set():
            self.id.value = count
            logger.info('Found expID {}, processing...'.format(count))
            self.running.set()
            proc = subprocess.Popen("sleep 30", shell=True)
            proc.wait()
            logger.info('ExpID {} finished.'.format(count))
            count += 1

        self.running.clear()
        self.id.value = 0
        logger.info("Bye!")

    def get_current_process_id(self):
        """ """
        return self.id.value

    def set_exit(self, value=True):
        """ """
        if value:
            self.exit.set()
        else:
            self.exit.clear()

    def get_exit(self):
        """ """
        return self.exit.is_set()


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class QLFAutomatic(object):
    def __init__(self):
        self.process = False

    def start(self):
        if self.process and self.process.is_alive():
            # se tem processo instanciado e ainda esta vivo, a flag 'exit' eh
            # desativada
            self.process.set_exit(False)
            logger.info("Monitor is already initialized (pid: %i)." % self.process.pid)
        else:
            # caso contrario a classe de monitoramento de exposures eh
            # instanciada e startada.
            self.process = QLFAutoRun()
            self.process.start()
            logger.info("Starting pid %i..." % self.process.pid)

    def stop(self):
        if self.process and self.process.is_alive():
            self.process.set_exit()
            # se tem processo instanciado e ainda esta vivo, o processo eh
            # interrompido
            logger.info("Stop pid %i" % self.process.pid)

            process_id = self.process.id.value
            pid = self.process.pid

            kill_proc_tree(pid, include_parent=False)

            logger.info('Delete {}?'.format(process_id))

            if process_id:
                QLFModels().delete_process(process_id)
        else:
            logger.info("Monitor is not initialized.")

    def reset(self):
        # interrompe o monitoramento de exposures
        self.stop()
        sleep(3)
        # deleta todo os processos do database
        logger.info('Delete ALL?')
        QLFModels().delete_all_processes()

    def get_status(self):
        status = False

        if self.process and not self.process.get_exit():
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
