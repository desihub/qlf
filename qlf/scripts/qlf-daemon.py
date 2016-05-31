#!/usr/bin/python
import time
from daemon import runner

class App():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/tmp/qlf-daemon.pid'
        self.pidfile_timeout = 5
    
    def run(self):
        while True:
            print("QLF daemon is running.")
            self.make_ql_config()
            time.sleep(60)
    
    def make_ql_config(self):
        pass

    def run_ql(self):
        pass

    def poll(self):
        pass

    def ingest(self):
        pass

app = App()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()
