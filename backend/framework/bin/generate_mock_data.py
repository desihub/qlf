from dashboard.models import Job, Process, QA, Exposure
import random
from datetime import datetime

class MockData():
    def __init__(self, base):
        self.base_process = Process.objects.get(pk=base)
        self.new_expid = 9999

    def generate_exposure(self):
        last_exposure = Exposure.objects.last()
        last_exposure.exposure_id = last_exposure.pk + 1
        last_exposure.save()
        last_exposure.telra = random.randint(1, 10000)/100
        last_exposure.teldec = random.randint(1, 10000)/100
        last_exposure.save()
        return last_exposure.exposure_id

    def generate_process(self, exposure_id):
        self.new_expid = exposure_id
        exposure = Exposure.objects.get(exposure_id=exposure_id)
        new_process = Process(
            start=datetime.now().replace(microsecond=0),
            end=datetime.now().replace(microsecond=0),
            status=self.base_process.status,
            exposure=exposure,
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
            self.generate_qas(job)

    def generate_qas(self, job):
        for qa in self.base_process.process_jobs.all()[0].job_qas.all():
            new_qa = QA(
                name=qa.name.replace(str(self.base_process.exposure_id), str(self.new_expid)),
                metrics=qa.metrics,
                params=qa.params,
                job=job,
                paname=qa.paname
            )
            new_qa.save()


# MockData(1).generate_exposure()
MockData(20).generate_process(3905)
