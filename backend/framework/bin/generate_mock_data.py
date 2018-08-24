import sys
import os
import django

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.append(os.path.join(BASE_DIR, "qlf"))

os.environ['DJANGO_SETTINGS_MODULE'] = 'qlf.settings'

django.setup()

from dashboard.models import Job, Process, QA, Exposure
import random
from datetime import datetime

class MockData():
    def generate_exposure(self):
        last_exposure = Exposure.objects.last()
        new_exposure = Exposure(
            exposure_id=last_exposure.pk+1,
            telra=random.randint(1, 10000)/100,
            teldec=random.randint(1, 10000)/100,
            tile=last_exposure.tile,
            dateobs=last_exposure.dateobs,
            flavor=last_exposure.flavor,
            night=last_exposure.night,
            airmass=last_exposure.airmass,
            program=last_exposure.program,
            exptime=last_exposure.exptime
        )
        new_exposure.save()
        return new_exposure.exposure_id

    def generate_process(self, base):
        self.base_process = Process.objects.get(pk=base)
        new_process = Process(
            start=datetime.now().replace(microsecond=0),
            end=datetime.now().replace(microsecond=0),
            status=self.base_process.status,
            exposure=self.base_process.exposure,
            qa_tests=self.base_process.qa_tests
        )
        new_process.save()
        self.generate_jobs(new_process)

    def generate_jobs(self, process):
        for job in self.base_process.process_jobs.all():
            new_job = Job(
                camera=job.camera,
                process=process,
                output=job.output,
                status=job.status,
                logname=job.logname,
                version=job.version
            )
            new_job.save()
            self.generate_qas(new_job)

    def generate_qas(self, job):
        for qa in self.base_process.process_jobs.get(camera=job.camera).job_qas.all():
            new_qa = QA(
                name=qa.name,
                metrics=qa.metrics,
                params=qa.params,
                job_id=job.pk,
                paname=qa.paname
            )
            new_qa.save()


MockData().generate_exposure()
# for i in range(100):
#     MockData().generate_process(3)
