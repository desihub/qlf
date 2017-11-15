import threading
import time
import schedule
import json
from .models import QlfState
from channels import Group

def job():
    state = QlfState.load()
    Group("monitor").send({
        "text": json.dumps({
            "daemon_status": state.daemon_status,
            "upstream_status": state.upstream_status,
        })
    })

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

def start_uptream():
    jobs = schedule.jobs
    if jobs == []:
        schedule.every(1).seconds.do(run_threaded, job)
        job_thread = threading.Thread(target=run_pending)
        job_thread.start()

def run_pending():
    while 1:
        schedule.run_pending()
        time.sleep(1)