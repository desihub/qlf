from ui_channel.camera_status import CameraStatus
from dashboard.models import Process, Job
from clients import get_exposure_monitoring
from dashboard.utils import get_date
import io
import os
import json
import logging
from log import get_logger
import datetime

desi_spectro_redux = os.environ.get('DESI_SPECTRO_REDUX')
qlf_root = os.environ.get('QLF_ROOT')

logger = get_logger(
    "qlf.qlf_state",
    os.path.join(qlf_root, "logs", "qlf_state.log")
)


class QLFState:
    def __init__(self):
        self.camera_status_generator = CameraStatus(self)
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
        self.exposure_id = str()
        self.qa_results = list()
        self.current_process_id = str()
        self.current_process = None
        self.available_cameras = list()
        self.diff_alerts = dict()
        self.camera_logs = dict()
        self.camera_status_generator.reset_camera_status()
        self.end_date = None

    def pipeline_end(self):
        if self.end_date is None and self.current_process.end is not None:
            self.end_date = self.current_process.end
            print(self.current_process)
            self.qa_results = self.camera_status_generator.get_qa_petals()
            if 'Fail' in str(self.qa_results) or \
               'Alarm' in str(self.qa_results):
                Process.objects.filter(id=self.current_process.id).update(
                    status=1
                )
            Process.objects.filter(id=self.current_process.id).update(
                qa_tests=self.qa_results
            )

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
            self.current_process = Process.objects.last()
        elif self.current_process_id is not str():
            self.current_process = Process.objects.last()
        else:
            return

        if self.current_process:
            self.update_pipeline_log()
            self.update_camera_logs()
            self.logfile = self.tail_file(os.path.join(
                qlf_root, "logs", "qlf.log"), 100)
            self.available_cameras = self.get_avaiable_cameras(
                self.current_process
            )
            self.exposure_id = self.current_process.exposure_id
            self.flavor = self.current_process.exposure.flavor
            self.current_process_id = self.current_process.id
            date = get_date(self.exposure_id)
            self.date_time = date.value if date else ''
            self.mjd = date.mjd if date else ''
            self.camera_status = self.camera_status_generator.get_camera_status()
            self.qa_results = self.camera_status_generator.get_qa_petals()
            self.pipeline_end()

    def get_current_state(self):
        return json.dumps({
            "pipeline_running": self.pipeline_running,
            "daemon_running": self.daemon_running,
            "exposure": self.exposure_id,
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
            "exposure": self.exposure_id,
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

        if self.old_state != new_state:
            self.old_state = new_state
            return new_state
        else:
            return None

    def get_avaiable_cameras(self, process):
        cams = list()
        for job in Job.objects.filter(process=self.current_process.id):
            cams.append(job.camera.camera)
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

        pipelinelog = os.path.join(qlf_root, "logs", "pipeline.log")

        try:
            return self.tail_file(pipelinelog, 100)
        except Exception as err:
            logger.error(err)
            return "Error"

    def get_camera_log(self, path):
        try:
            arq = open(path, 'r')
            log = arq.readlines()
            return log
        except Exception:
            return ["File not found"]

    def update_camera_logs(self):
        for job in Job.objects.filter(process=self.current_process.id):
            camera = job.camera
            camera_log_path = os.path.join(
                desi_spectro_redux,
                job.logname
            )
            self.camera_logs[camera.camera] = self.get_camera_log(camera_log_path)
