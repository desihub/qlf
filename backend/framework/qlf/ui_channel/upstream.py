import threading
import time
import schedule
import json
from channels import Group
import Pyro4
from django.conf import settings
from .views import open_file
import subprocess
import os
import sys
import configparser
import requests
from ui_channel.camera_status import get_camera_status
from dashboard.utils import get_date
from astropy.io import fits
from astropy.time import Time
import logging
import io

from dashboard.bokeh.helper import get_last_process
import Pyro4

uri = settings.QLF_DAEMON_URL
qlf = Pyro4.Proxy(uri)

qlf_root = os.getenv('QLF_ROOT')
cfg = configparser.ConfigParser()

logger = logging.getLogger()

try:
    cfg.read('%s/framework/config/qlf.cfg' % qlf_root)
    desi_spectro_redux = cfg.get('namespace', 'desi_spectro_redux')
    desi_spectro_data = cfg.get('namespace', 'desi_spectro_data')
    night = cfg.get('data', 'night')
except Exception as error:
    logger.error(error)
    logger.error("Error reading  %s/framework/config/qlf.cfg" % qlf_root)

class Upstream:
    def __init__(self):
        self.startedUpStreamJob = False

    def get_date(self, exp):
        # open file
        exp_zfill = str(exp).zfill(8)
        fits_file = '{}/{}/desi-{}.fits.fz'.format(desi_spectro_data, night, exp_zfill)

        f = fits.open(fits_file)

        # read the time in isot
        time = f[0].header['DATE-OBS']

        # declare the format
        t = Time(time, format='isot', scale='utc')

        # Convert to MJD
        return t


    def get_camera_log(self, cam):
        process = get_last_process()
        cameralog = None

        try:
            for item in process[0].get("process_jobs"):
                if cam == item.get("camera"):
                    cameralog = os.path.join(desi_spectro_redux, item.get('logname'))
                    break
            if cameralog:
                arq = open(cameralog, 'r')
                log = arq.readlines()
                return log

        except Exception as err:
            logger.error(err)
            return "Error"


    def get_pipeline_log(self):
        """ Gets pipeline log """

        pipelinelog = cfg.get('main', 'logpipeline')

        try:
            return self.tail_file(pipelinelog, 100)
        except Exception as err:
            logger.error(err)
            return "Error"


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


    def avaiable_cameras(self, process):
        if len(process) != 0:
            cams = list()
            for job in process[0]['process_jobs']:
                cams.append(job['camera'])
            return cams
        return list()

    uri = settings.QLF_DAEMON_URL
    qlf = Pyro4.Proxy(uri)

    def start_daemon(self):
        qlf.start()

    def stop_daemon(self):
        qlf.stop()

    def reset_daemon(self):
        qlf.reset()

    def get_current_state(self):
        camera_status = get_camera_status()
        process = get_last_process()
        qa_results = self.get_current_qa_tests(process)
        available_cameras = self.avaiable_cameras(process)
        daemon_status = qlf.get_status()
        logfile = self.tail_file(open_file('logfile'), 100)

        if daemon_status:
            if not qlf.is_running():
                daemon_status = None

        pipelinelog = list()
        mjd = str()
        process_id = int()
        date = dict()
        date_time = str()
        if len(process) > 0:
            pipelinelog = self.get_pipeline_log()
            exposure = process[0].get("exposure")
            process_id = process[0].get("id")
            date = self.get_date(exposure)
            date_time = date.value
            mjd = date.mjd
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

    def get_current_qa_tests(self, process):
        if process != []:
            qa_tests = qlf.qa_tests(process[0]['id'])
            return { 'qa_tests': qa_tests }
        else:
            return { 'Error': 'Missing process_id' }

    def job(self):
        state = self.get_current_state()

        Group("monitor").send({
            "text": state
        })


    def run_threaded(self, job_func):
        job_thread = threading.Thread(target=job_func)
        job_thread.start()


    def start_uptream(self):
        if self.startedUpStreamJob == False:
            schedule.every(3).seconds.do(self.run_threaded, self.job)
            job_thread = threading.Thread(target=self.run_pending)
            job_thread.start()
        self.startedUpStreamJob = True

    def run_pending(self):
        while 1:
            schedule.run_pending()
            time.sleep(3)
