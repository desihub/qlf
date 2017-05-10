import os
import sys
import argparse
import yaml
import json
import numpy
import requests
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
    """ """

    # def __init__(self):
    #     """ """
    #
    #     self.session = requests.Session()
    #     self.session.headers['Content-Type'] = 'application/json'
    #     self.session.auth = HTTPBasicAuth('nobody', 'nobody')
    #     self.baseurl = QLF_API_URL

    def insert_exposure(self, expid, night):
        """ """

        # Check if expid is already registered
        if not Exposure.objects.filter(expid=expid):
            exposure = Exposure(expid=expid, night=night)
            exposure.save()
            print("Registered exposure {}".format(expid))

        # Save Process for this exposure
        return Exposure.objects.get(expid=expid)

    def insert_process(self, expid, night, pipeline_name):
        """ """

        exposure = self.insert_exposure(expid, night)

        process = Process(
            exposure_id=exposure.expid,
            pipeline_name=pipeline_name
        )

        process.save()

        return process

    def insert_config(self, process_id):
        """ """

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
        """ """

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
        """ """

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
        """ """

        process = Process.objects.filter(id=process_id).update(
            end=end,
            status=status
        )

        print("UPDATE PROCESS: %s" % process)

        return process

    def update_job(self, job_id, end, status):
        """ """

        job = Job.objects.filter(id=job_id).update(
            end=end,
            status=status
        )

        print("UPDATE JOB: %s" % job)

        return job

    def insert_qa(self, qa_obj, force=False):
        """ Insert or update qa table """

        name = qa_obj['name']
        expid = qa_obj['expid']
        camera = qa_obj['camera']

        if not QA.objects.filter(name=name):
            # Register for QA results for the first time
            qa = QA(
                name=name,
                description=qa_obj['description'],
                paname=qa_obj['paname'],
                metric=qa_obj['metric'],
                job_id=qa_obj['job_id']
            )
            qa.save()
            print("Saved {} results for exposure={} and camera={}".format(
                name, expid, camera
            ))
            print("See {}".format(QLF_API_URL))
        elif force:
            # Overwrite QA results
            QA.objects.filter(name=name).update(
                job_id=qa_obj['job_id'],
                description=qa_obj['description'],
                paname=qa_obj['paname'],
                metric=qa_obj['metric']
            )
            print("Overwritten {} results for exposure={} and camera={}".format(
                name, expid, camera
            ))
        else:
            print(
                "{} results for exposure={} and camera={} already "
                "registered. Use --force to overwrite.".format(
                    name, expid, camera
            ))

    def post(self, name, job_name, results, force=False):

        if name not in results:
            print('{} metric not found in {}'.format(name, results))

        qa = results[name]

        try:
            expid = qa['EXPID']
            arm = qa['ARM']
            spectrograph = qa['SPECTROGRAPH']
            paname = qa['PANAME']
            value = self.jsonify(qa['VALUE'])
        except:
            print(
                "Fatal: unexpected format for QA file. "
                "Looking for 'EXPID', 'ARM', 'SPECTROGRAPH', "
                "'PANAME' and 'VALUE' keys."
            )
            sys.exit(1)


        camera_name = arm + str(spectrograph)

        camera = self.insert_camera({
            'camera': camera_name,
            'arm': arm,
            'spectrograph': spectrograph
        })

        process = self.insert_process(expid)

        configuration = self.insert_config(process.id)

        job = self.insert_job({
            'name': job_name,
            'process_id': process.id,
            'camera_id': camera
        })

        qa_obj = {
            'name': name,
            'description': '',
            'paname': paname,
            'metric': value,
            'job_id': job.id,
            'camera': camera,
            'expid': expid
        }

        self.insert_qa(qa_obj, force)

    def jsonify(self, data):
        ''' Make a dictionary with numpy arrays JSON serializable'''

        for key in data:
            if type(data[key]) == numpy.ndarray:
                data[key] = data[key].tolist()
        return data

    def close(self):
        """ Finalize session """
        self.session.close()

if __name__=='__main__':

    parser = argparse.ArgumentParser(
        description="""Upload QA metrics produced by the Quick Look pipeline to QLF database.
This script is meant to be run from the command line or imported by Quick Look. """,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
            '--file',
            dest='file',
            required=True,
            help='Path to QA file produced by Quick Look')

    parser.add_argument(
            '--qa-name',
            dest='qa_name',
            required=True,
            help='Name of the QA metric to be ingested'
    )

    parser.add_argument(
            '--force',
            default=False,
            action='store_true',
            help='Overwrite QA results for a given metric'
    )

    qa_name = parser.parse_args().qa_name

    file = parser.parse_args().file

    job_name = os.path.basename(file)

    results = yaml.load(open(file, 'r'))

    force = parser.parse_args().force

    qlfi = QLFIngest()

    qlfi.post(qa_name, job_name, results, force)


