from ui_channel.camera_status import get_camera_status
from dashboard.bokeh.helper import get_current_process
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
        self.reset_state()
        self.update_qlf_status()
        if self.pipeline_running is False or self.pipeline_running is None:
            self.daemon_running = False
        else:
            self.daemon_running = True

    def set_daemon_running(self, status, current_process_id):
        self.daemon_running = status
        self.current_process_id = current_process_id

    def reset_state(self):
        self.camera_status = {"b": list(), "r": list(), "z": list()}
        self.logfile = list()
        self.pipelinelog = list()
        self.mjd = str()
        self.date_time = str()
        self.pipeline_running = False
        self.daemon_running = False
        self.exposure = str()
        self.qa_results = list()
        self.current_process_id = str()
        self.current_process = list()
        self.available_cameras = list()

    def update_qlf_status(self):
        qlf = get_exposure_monitoring()
        self.pipeline_running = qlf.get_status()
        if self.pipeline_running:
            if not qlf.is_running():
                self.pipeline_running = None

    def update_qlf_state(self):
        self.update_qlf_status()
        if self.daemon_running:
            self.update_current_process()

    def update_current_process(self):
        if self.current_process_id is not -2:
            self.current_process = get_current_process()

        if len(self.current_process) > 0:
            self.pipelinelog = self.get_pipeline_log()
            self.logfile = self.tail_file(open_file('logfile'), 100)
            self.camera_status = get_camera_status()
            self.available_cameras = self.get_avaiable_cameras(
                self.current_process[0]
            )
            self.exposure = self.current_process[0]["exposure"]
            self.qa_results = self.current_process[0].get("qa_tests")
            self.current_process_id = self.current_process[0].get("id")
            date = get_date(self.exposure) if self.exposure else None
            self.date_time = date.value if date else ''
            self.mjd = date.mjd if date else ''

    def get_current_state(self):
        self.update_qlf_state()

        return json.dumps({
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
            "process_id": self.current_process_id
        })

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
