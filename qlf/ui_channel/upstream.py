import threading
import time
import schedule
import json
from .models import QlfState
from channels import Group
import Pyro4
from django.conf import settings
from .views import open_file
import subprocess
import os
import configparser
import requests
from ui_channel.camera_status import get_camera_status

from dashboard.bokeh.helper import get_last_process

qlf_root = os.getenv('QLF_ROOT')
cfg = configparser.ConfigParser()

try:
    cfg.read('%s/qlf/config/qlf.cfg' % qlf_root)
    desi_spectro_redux = cfg.get('namespace', 'desi_spectro_redux')
except Exception as error:
    logger.error(error)
    logger.error("Error reading  %s/qlf/config/qlf.cfg" % qlf_root)

def get_camera_log(cam):
    process = get_last_process()
    cameralog = None
    log = str()
    try:
        for item in process[0].get("process_jobs"):
            if cam == item.get("camera"):
                cameralog = os.path.join(desi_spectro_redux, item.get('logname'))
                break
        if cameralog:
            arq = open(cameralog, 'r')
            log = arq.readlines()
            return log

    except Exception as e:
        print(e)
        return "Error"

uri = settings.QLF_DAEMON_URL
qlf = Pyro4.Proxy(uri)

uri_manual = settings.QLF_MANUAL_URL
qlf_manual = Pyro4.Proxy(uri_manual)

def start_daemon():
    start_url = settings.QLF_BASE_URL + '/start'
    requests.get(start_url)

def stop_daemon():
    stop_url = settings.QLF_BASE_URL + '/stop'
    requests.get(stop_url)

def get_current_state():
    camera_status = get_camera_status()
    state = QlfState.load()
    process = get_last_process()
    if qlf.get_status() != state.daemon_status:
        state.daemon_status = qlf.get_status()
        state.save()

    logfile = open_file('logfile')
    if len(process) > 0:
        exposure = process[0].get("exposure")
    else:
        exposure = ''

    lines = subprocess.check_output(['tail', '-100', logfile])
    lines_array = lines.strip().decode('utf-8').split("\n")
    return json.dumps({
            "daemon_status": state.daemon_status,
            "upstream_status": state.upstream_status,
            "lines": lines_array,
            "exposure": exposure,
            "cameras": camera_status,
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