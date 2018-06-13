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
    def get_current_state(self):
        camera_status = get_camera_status()
        process = get_current_process()
        available_cameras = self.avaiable_cameras(process)
        qlf = get_exposure_monitoring()
        daemon_status = qlf.get_status()
        logfile = self.tail_file(open_file('logfile'), 100)

        if daemon_status:
            if not qlf.is_running():
                daemon_status = None

        pipelinelog = list()
        mjd = str()
        process_id = int()
        date_time = str()
        qa_results = list()
        if len(process) > 0:
            pipelinelog = self.get_pipeline_log()
            exposure = process[0].get("exposure")
            qa_results = process[0].get("qa_tests")
            process_id = process[0].get("id")
            date = get_date(exposure)
            date_time = date.value if date else ''
            mjd = date.mjd if date else ''
        else:
            exposure = ''
        return json.dumps({
            "daemon_status": daemon_status,
            "exposure": exposure,
            "cameras": camera_status,
            "available_cameras": available_cameras,
            "qa_results": qa_results,
            "lines": logfile,
            "ingestion": pipelinelog,
            "mjd": mjd,
            "date": date_time,
            "process_id": process_id
        })

    def avaiable_cameras(self, process):
        if len(process) != 0:
            cams = list()
            for job in process[0]['process_jobs']:
                cams.append(job['camera'])
            return cams
        return list()

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
