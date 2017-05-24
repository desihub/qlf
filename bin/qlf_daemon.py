from dos_monitor import DOSmonitor
from qlf_pipeline import QLFPipeline
from time import sleep
from multiprocessing import Process, Event
from dashboard.bokeh.helper import get_last_exposures_by_night

import Pyro4
import configparser
import sys
import os


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class QLFDaemon(object):
    def __init__(self):
        self.run = QLFRun()

    def start(self):
        if self.run.is_alive():
            message = "Monitor is already initialized (pid: %i)." % self.run.pid
        else:
            self.run = QLFRun()
            self.run.start()
            message = "Starting pid %i..." % self.run.pid

        print(message)

    def stop(self):
        if self.run.is_alive():
            message = "Stop pid %i" % self.run.pid
            self.run.shutdown()
        else:
            message = "Monitor is not initialized."

        print(message)

    def restart(self):
        self.stop()
        print("Restarting...")
        sleep(5)
        self.start()


class QLFRun(Process):

    def __init__(self):
        Process.__init__(self)
        self.exit = Event()
        self.dos_monitor = DOSmonitor()
        # TODO: get last night from db (improve)
        self.last_night = get_last_exposures_by_night().get('night', '')

    def run(self):
        while not self.exit.is_set():
            night = self.dos_monitor.get_last_night()

            if night == self.last_night:
                print("The night %s has already been processed" % night)
                sleep(5)
                continue

            exposures = self.dos_monitor.get_exposures_by_night(night)

            for exposure in exposures:
                if self.exit.is_set():
                    print('Execution stopped')
                    break

                ql = QLFPipeline(exposure)
                ql.start_process()
                print('Executing expid %s...' % exposure.get('expid'))

            self.last_night = night

        print("Bye!")

    def shutdown(self):
        self.exit.set()

def main():

    qlf_root = os.getenv('QLF_ROOT')
    cfg = configparser.ConfigParser()

    try:
        cfg.read('%s/qlf/config/qlf.cfg' % qlf_root)
        nameserver = cfg.get("daemon", "nameserver")
        host = cfg.get("daemon", "host")
        port = int(cfg.get("daemon", "port"))
    except Exception as error:
        print(error)
        print("Error reading  %s/qlf/config/qlf.cfg" % qlf_root)
        sys.exit(1)

    Pyro4.Daemon.serveSimple(
        {QLFDaemon: nameserver},
        host=host,
        port=port,
        ns=False
    )

if __name__ == "__main__":
    main()
