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
        last_process = Process.objects.last()
        last_process.pk = None
        last_process.save()
        last_process.exposure_id = exposure_id
        last_process.start = datetime.now().replace(microsecond=0)
        last_process.end = datetime.now().replace(microsecond=0)
        last_process.save()
        print(last_process.pk)
        self.generate_jobs(last_process.pk)

    def generate_jobs(self, process_id):
        for job in self.base_process.process_jobs.all():
            job.pḱ = None
            job.save()
            job.process_id = process_id
            job.save()
            self.generate_qas(job.pk)

    def generate_qas(self, job_id):
        for qa in self.base_process.process_jobs.all()[0].job_qas.all():
            qa.pk = None
            qa.save()
            qa.job_id = job_id
            qa.name = qa.name.replace(str(self.base_process.exposure_id), str(self.new_expid))
            qa.save()


MockData(20).generate_process(3910)
# MockData().generate_exposure()
