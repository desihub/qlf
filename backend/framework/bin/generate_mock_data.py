import sys
import os
import django

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.append(os.path.join(BASE_DIR, "qlf"))

os.environ['DJANGO_SETTINGS_MODULE'] = 'qlf.settings'

django.setup()

from dashboard.models import Job, Process, Exposure
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
                end=datetime.now().replace(microsecond=0),
                start=datetime.now().replace(microsecond=0),
                output=job.output,
                status=job.status,
                logname=job.logname,
                version=job.version
            )
            new_job.save()

#MockData().generate_exposure()
# for i in range(100):
#     MockData().generate_process(3)

from qlf_models import QLFModels
from copy import copy
import datetime
import random

qlf_models = QLFModels()


def generate_processes_by_exposure(exposure, loop=1):
    """ """

    flavor = exposure.flavor

    process = qlf_models.get_last_process_by_flavor(flavor)

    if not process:
        raise ValueError(
            'There is no process with {} flavor.'.format(flavor)
        )

    origin_process = copy(process)

    for item in range(loop):
        del process.id
        process.exposure_id = exposure.exposure_id
        process.save()


def generate_new_exposure(flavor, night):
    """ """

    last_exp = qlf_models.get_last_exposure()
    exposure = qlf_models.get_last_exposure_by_flavor(flavor)

    if not exposure:
        raise ValueError(
            'There is no exposure with {} flavor.'.format(flavor)
        )

    exposure.exposure_id = last_exp.exposure_id + 1
    exposure.night = night
    tdate = datetime.datetime.strptime(night, "%Y%m%d")
    tdate += datetime.timedelta(hours=random.randint(1, 23))
    exposure.dateobs = tdate
    exposure.save()

    return exposure


new_exposure = generate_new_exposure('science', '20181001')
print(new_exposure)
# generate_processes_by_exposure(new_exposure)