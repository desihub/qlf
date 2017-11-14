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
            "state": state.running,
        })
    })

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

def start_uptream():
    schedule.every(1).seconds.do(run_threaded, job)
    job_thread = threading.Thread(target=run_pending)
    job_thread.start()

def run_pending():
    while 1:
        schedule.run_pending()
        time.sleep(1)