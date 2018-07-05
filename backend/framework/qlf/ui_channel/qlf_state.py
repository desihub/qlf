from ui_channel.camera_status import CameraStatus
from dashboard.bokeh.helper import get_monitor_process
from clients import get_exposure_monitoring
from .views import open_file
from util import get_config
from dashboard.utils import get_date
import io
import os
import json
import logging

logger = logging.getLogger()


class QLFState:
    def __init__(self):
        self.camera_status_generator = CameraStatus()
        self.reset_state()
        self.update_pipeline_status()
        if self.pipeline_running is 0:
            self.daemon_running = False
        else:
            self.daemon_running = True

    def update_pipeline_log(self):
        self.pipelinelog = self.get_pipeline_log()

    def set_daemon_running(self, status):
        self.daemon_running = status
        if status:
            self.reset_state()
            self.pipeline_running = 1
            self.daemon_running = True
        else:
            self.update_pipeline_log()
            self.pipeline_running = 0

    def reset_state(self):
        self.camera_status = {"b": list(), "r": list(), "z": list()}
        self.old_state = dict()
        self.logfile = list()
        self.pipelinelog = list()
        self.mjd = str()
        self.flavor = str()
        self.date_time = str()
        self.pipeline_running = 0
        self.daemon_running = False
        self.exposure = str()
        self.qa_results = list()
        self.current_process_id = str()
        self.current_process = None
        self.available_cameras = list()
        self.diff_alerts = dict()
        self.camera_status_generator.reset_camera_status()

    def update_pipeline_status(self):
        """
        0: Not Running
        1: Idle
        2: Running
        """
        qlf = get_exposure_monitoring()
        self.pipeline_running = 0 if not qlf.get_status() else 2
        if self.pipeline_running:
            if not qlf.is_running():
                self.pipeline_running = 1

    def update_qlf_state(self):
        self.update_pipeline_status()
        if self.daemon_running and self.pipeline_running is not 0:
            self.update_current_process()

    def update_current_process(self):
        if self.pipeline_running is 2:
            process = get_monitor_process(None)
            if len(process) > 0:
                self.current_process = process[0]
        elif self.current_process_id is not str():
            self.current_process = get_monitor_process(self.current_process_id)
        else:
            return

        if 'detail' not in self.current_process:
            self.update_pipeline_log()
            self.logfile = self.tail_file(open_file('logfile'), 100)
            self.available_cameras = self.get_avaiable_cameras(
                self.current_process
            )
            self.exposure = self.current_process["exposure"]
            self.flavor = self.current_process.get("flavor")
            self.current_process_id = self.current_process.get("id")
            date = get_date(self.exposure) if self.exposure else None
            self.date_time = date.value if date else ''
            self.mjd = date.mjd if date else ''
            self.camera_status = self.camera_status_generator.get_camera_status(
                self.current_process
            )
            self.qa_results = self.camera_status_generator.get_qa_petals()

    def get_current_state(self):
        return json.dumps({
            "pipeline_running": self.pipeline_running,
            "daemon_running": self.daemon_running,
            "exposure": self.exposure,
            "flavor": self.flavor,
            "cameras": self.camera_status,
            "available_cameras": self.available_cameras,
            "qa_results": self.qa_results,
            "lines": self.logfile,
            "ingestion": self.pipelinelog,
            "mjd": self.mjd,
            "date": self.date_time,
            "process_id": self.current_process_id
        })

    def get_monitor_state(self):
        self.update_qlf_state()

        new_state = json.dumps({
            "pipeline_running": self.pipeline_running,
            "daemon_running": self.daemon_running,
            "exposure": self.exposure,
            "cameras": self.camera_status,
            "available_cameras": self.available_cameras,
            "qa_results": self.qa_results,
            "lines": self.logfile,
            "ingestion": self.pipelinelog,
            "mjd": self.mjd,
            "date": self.date_time,
            "flavor": self.flavor,
            "process_id": self.current_process_id
        })

        # return new_state

        if self.old_state != new_state:
            self.old_state = new_state
            return new_state
        else:
            return None

    def get_avaiable_cameras(self, process):
        cams = list()
        for job in process['process_jobs']:
            cams.append(job['camera'])
        return cams

    def tail_file(self, filename, number_lines):
        with io.open(filename) as logfile:
            logfile.seek(0, os.SEEK_END)
            endf = position = logfile.tell()
            linecnt = 0

            while position >= 0:
                logfile.seek(position)
                next_char = logfile.read(1)

                if next_char == "\n" and position != endf-1:
                    linecnt += 1

                if linecnt == number_lines:
                    break
                position -= 1

            if position < 0:
                logfile.seek(0)

            log_lines = logfile.readlines()

        return log_lines

    def get_pipeline_log(self):
        """ Gets pipeline log """
        cfg = get_config()

        pipelinelog = cfg.get('main', 'logpipeline')

        try:
            return self.tail_file(pipelinelog, 100)
        except Exception as err:
            logger.error(err)
            return "Error"
