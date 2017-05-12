import os
import sys
import yaml
import json
import numpy
# import argparse

from django.core.wsgi import get_wsgi_application

QLF_API_URL = os.environ.get(
    'QLF_API_URL',
    'http://localhost:8000/dashboard/api'
)

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.append(os.path.join(BASE_DIR, "qlf"))

os.environ['DJANGO_SETTINGS_MODULE'] = 'qlf.settings'

application = get_wsgi_application()

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
            print("Registered exposure {}".format(expid))

        # Save Process for this exposure
        return Exposure.objects.get(expid=expid)

    def insert_process(self, expid, night, pipeline_name):
        """ Inserts initial data in process table. """

        exposure = self.insert_exposure(expid, night)

        process = Process(
            exposure_id=exposure.expid,
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
            print("Registered camera {}".format(camera_obj))

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
            print("Save {} results".format(name))
            print("See {}".format(QLF_API_URL))
        elif force:
            # Overwrite QA results
            QA.objects.filter(name=name).update(
                job_id=job_id,
                description='',
                paname=paname,
                metric=metrics
            )
            print("Overwritten {} results".format(name))
            print("See {}".format(QLF_API_URL))
        else:
            print(
                "{} results already registered. "
                "Use --force to overwrite.".format(name)
            )

    def jsonify(self, data):
        """ Make a dictionary with numpy arrays JSON serializable """

        for key in data:
            if type(data[key]) == numpy.ndarray:
                data[key] = data[key].tolist()
        return data

    # def post(self, name, job_name, results, force=False):
    #
    #     if name not in results:
    #         print('{} metric not found in {}'.format(name, results))
    #
    #     qa = results[name]
    #
    #     try:
    #         expid = qa['EXPID']
    #         arm = qa['ARM']
    #         spectrograph = qa['SPECTROGRAPH']
    #         paname = qa['PANAME']
    #         value = self.jsonify(qa['VALUE'])
    #     except:
    #         print(
    #             "Fatal: unexpected format for QA file. "
    #             "Looking for 'EXPID', 'ARM', 'SPECTROGRAPH', "
    #             "'PANAME' and 'VALUE' keys."
    #         )
    #         sys.exit(1)
    #
    #
    #     camera_name = arm + str(spectrograph)
    #
    #     camera = self.insert_camera({
    #         'camera': camera_name,
    #         'arm': arm,
    #         'spectrograph': spectrograph
    #     })
    #
    #     process = self.insert_process(expid)
    #
    #     configuration = self.insert_config(process.id)
    #
    #     job = self.insert_job({
    #         'name': job_name,
    #         'process_id': process.id,
    #         'camera_id': camera
    #     })
    #
    #     qa_obj = {
    #         'name': name,
    #         'description': '',
    #         'paname': paname,
    #         'metric': value,
    #         'job_id': job.id,
    #         'camera': camera,
    #         'expid': expid
    #     }
    #
    #     self.insert_qa(qa_obj, force)

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

