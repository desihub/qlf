import os
import sys
import yaml
import json
import numpy

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.append(os.path.join(BASE_DIR, "qlf"))

os.environ['DJANGO_SETTINGS_MODULE'] = 'qlf.settings'

import django
django.setup()

from dashboard.models import (
    Job, Exposure, Camera, QA, Process, Configuration
)


class QLFIngest(object):
    """ Class responsable by results ingestion from Quick Look pipeline. """

    def insert_exposure(self, expid, night):
        """ Inserts and gets exposure and night if necessary. """

        # Check if expid is already registered
        if not Exposure.objects.filter(expid=expid):
            exposure = Exposure(expid=expid, night=night)
            exposure.save()

        # Save Process for this exposure
        return Exposure.objects.get(expid=expid)

    def insert_process(self, expid, night, start, pipeline_name):
        """ Inserts initial data in process table. """

        exposure = self.insert_exposure(expid, night)

        process = Process(
            exposure_id=exposure.expid,
            start=start,
            pipeline_name=pipeline_name
        )

        process.save()

        return process

    def insert_config(self, process_id):
        """ Inserts used configuration. """

        #TODO: get configuration coming of interface
        # Make sure there is a configuration to refer to
        if not Configuration.objects.all():
            config_file = open('../qlf/static/ql.json', 'r')
            config_str = config_file.read()
            config_file.close()

            config_json = self.jsonify(json.loads(config_str))

            configuration = Configuration(
                configuration=config_json,
                process_id=process_id
            )

            configuration.save()

        return Configuration.objects.latest('pk')

    def insert_camera(self, camera):
        """ Inserts used camera. """

        # Check if camera is already registered
        if not Camera.objects.filter(camera=camera):
            camera_obj = Camera(
                camera=camera,
                arm=camera[0],
                spectrograph=camera[-1]
            )
            camera_obj.save()

        # Save Job for this camera
        return Camera.objects.get(camera=camera)

    def insert_job(self, process_id, camera, start, logname, version='1.0'):
        """ Insert job and camera if necessary. """

        camera = self.insert_camera(camera)

        job = Job(
            process_id=process_id,
            camera_id=camera,
            start=start,
            logname=logname,
            version=version
        )
        job.save()

        return job

    def update_process(self, process_id, end, status):
        """ Updates process with execution results. """

        process = Process.objects.filter(id=process_id).update(
            end=end,
            status=status
        )

        return process

    def update_job(self, job_id, end, status):
        """ Updates job with execution results. """

        job = Job.objects.filter(id=job_id).update(
            end=end,
            status=status
        )

        return job

    def insert_qa(self, name, paname, metrics, job_id, force=False):
        """ Inserts or updates qa table """

        metrics = self.jsonify(metrics)

        if not QA.objects.filter(name=name):
            # Register for QA results for the first time
            qa = QA(
                name=name,
                description='',
                paname=paname,
                metric=metrics,
                job_id=job_id
            )
            qa.save()
        elif force:
            # Overwrite QA results
            QA.objects.filter(name=name).update(
                job_id=job_id,
                description='',
                paname=paname,
                metric=metrics
            )
        else:
            print(
                "{} results already registered. "
                "Use --force to overwrite.".format(name)
            )

    def get_expid_in_process(self, expid):
        """ gets process object by expid """

        return Process.objects.filter(exposure_id=expid)

    def jsonify(self, data):
        """ Make a dictionary with numpy arrays JSON serializable """

        for key in data:
            if type(data[key]) == numpy.ndarray:
                data[key] = data[key].tolist()
        return data

if __name__=='__main__':
    qlf = QLFIngest()
 

# TODO: implement command line interface for qlf_ingest.py

# if __name__=='__main__':
#
#     parser = argparse.ArgumentParser(
#         description="""Upload QA metrics produced by the Quick Look pipeline to QLF database.
# This script is meant to be run from the command line or imported by Quick Look. """,
#         formatter_class=argparse.RawDescriptionHelpFormatter)
#
#     parser.add_argument(
#             '--file',
#             dest='file',
#             required=True,
#             help='Path to QA file produced by Quick Look')
#
#     parser.add_argument(
#             '--qa-name',
#             dest='qa_name',
#             required=True,
#             help='Name of the QA metric to be ingested'
#     )
#
#     parser.add_argument(
#             '--force',
#             default=False,
#             action='store_true',
#             help='Overwrite QA results for a given metric'
#     )
#
#     qa_name = parser.parse_args().qa_name
#
#     file = parser.parse_args().file
#
#     job_name = os.path.basename(file)
#
#     results = yaml.load(open(file, 'r'))
#
#     force = parser.parse_args().force
#
#     qlfi = QLFIngest()
#
#     qlfi.post(qa_name, job_name, results, force)

