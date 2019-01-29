import threading
import time
import schedule
from channels import Group
import os
import logging
from log import get_logger
from ui_channel.alerts import Alerts
import json
from clients import get_exposure_monitoring

from log import get_logger

qlf_root = os.environ.get('QLF_ROOT')

log = get_logger(
    "qlf.upstream",
    os.path.join(qlf_root, "logs", "upstream.log")
)

alerts = Alerts()

qlf = get_exposure_monitoring()

logger = logging.getLogger()

desi_spectro_data = os.environ.get('DESI_SPECTRO_DATA')
desi_spectro_redux = os.environ.get('DESI_SPECTRO_REDUX')
loglevel = os.environ.get('PIPELINE_LOGLEVEL')
logpipeline = os.path.join(qlf_root, "logs", "pipeline.log")
logger_pipeline = get_logger("pipeline", logpipeline, loglevel)


class Upstream:
    def __init__(self, qlf_state):
        self.startedUpStreamJob = False
        self.qlf_state = qlf_state
        self.updating = False

    def start_daemon(self):
        qlf.start()
        self.qlf_state.set_daemon_running(True)

    def stop_daemon(self):
        qlf.stop()
        self.qlf_state.set_daemon_running(False)

    def reset_daemon(self):
        qlf.reset()

    def pipeline_message(self, message):
        logger_pipeline.info(message)

    def monitor_job(self):
        if not self.updating:
            self.updating = True
            state = self.qlf_state.get_monitor_state()

            if state is not None:
                Group("monitor").send({
                    "text": state
                })
            self.updating = False

    def disk_space_job(self):
        Group("monitor").send({
            "text": json.dumps({
                "notification": alerts.available_space()
            })
        })

    def update_camera_log(self):
        for cam in self.qlf_state.camera_logs.keys():
            Group(cam).send({
                "text": json.dumps({
                    "cameralog": self.qlf_state.camera_logs[cam]
                })
            })

    def start_uptream(self):
        if not self.startedUpStreamJob:
            schedule.every(int(
                os.environ.get('WEBSOCKET_UPDATE_INTERVAL', 3)
            )).seconds.do(self.monitor_job)
            schedule.every(30).minutes.do(
                self.disk_space_job
            )
            schedule.every(8).seconds.do(
                self.update_camera_log
            )
            job_thread = threading.Thread(target=self.run_pending)
            job_thread.start()
        self.startedUpStreamJob = True

    def run_pending(self):
        while 1:
            schedule.run_pending()
            time.sleep(1)
