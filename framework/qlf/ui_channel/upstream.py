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
from astropy.io import fits
from astropy.time import Time
import logging
import io

from dashboard.bokeh.helper import get_last_process, get_cameras

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


def get_date(exp):
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


def get_camera_log(cam):
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


def get_pipeline_log():
    """ Gets pipeline log """

    pipelinelog = cfg.get('main', 'logpipeline')

    try:
        return tail_file(pipelinelog, 100)
    except Exception as err:
        logger.error(err)
        return "Error"


def tail_file(filename, number_lines):

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


def avaiable_cameras(process):
    if len(process) != 0:
        cams = list()
        for job in process[0]['process_jobs']:
            cams.append(job['camera'])
        return cams
    return list()

uri = settings.QLF_DAEMON_URL
qlf = Pyro4.Proxy(uri)

def start_daemon():
    qlf.start()

def stop_daemon():
    qlf.stop()

def reset_daemon():
    qlf.reset()

def get_current_state():
    camera_status = get_camera_status()
    qa_results = get_cameras()
    process = get_last_process()
    available_cameras = avaiable_cameras(process)
    daemon_status = qlf.get_status()

    logfile = open_file('logfile')
    pipelinelog = list()
    mjd = str()
    date = dict()
    date_time = str()
    if len(process) > 0:
        pipelinelog = get_pipeline_log()
        exposure = process[0].get("exposure")
        date = get_date(exposure)
        date_time = date.value
        mjd = date.mjd
    else:
        exposure = ''

    lines = subprocess.check_output(['tail', '-100', logfile])
    lines_array = lines.strip().decode('utf-8').split("\n")
    return json.dumps({
            "daemon_status": daemon_status,
            "lines": lines_array,
            "exposure": exposure,
            "cameras": camera_status,
            "available_cameras": available_cameras,
            "qa_results": qa_results,
            "ingestion": pipelinelog,
            "mjd": mjd,
            "date": date_time
        })


def job():
    state = get_current_state()

    Group("monitor").send({
        "text": state
    })


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


def start_uptream():
    jobs = schedule.jobs
    if jobs == []:
        schedule.every(3).seconds.do(run_threaded, job)
        job_thread = threading.Thread(target=run_pending)
        job_thread.start()


def run_pending():
    while 1:
        schedule.run_pending()
        time.sleep(3)
