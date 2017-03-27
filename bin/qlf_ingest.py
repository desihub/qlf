import os
import sys
import argparse
import yaml
import json
import numpy
from django.core.wsgi import get_wsgi_application

QLF_API_URL = os.environ.get('QLF_API_URL',
                             'http://localhost:8000/dashboard/api')
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.append(os.path.join(BASE_DIR, "qlf"))

os.environ['DJANGO_SETTINGS_MODULE'] = 'qlf.settings'

application = get_wsgi_application()

from dashboard.models import (
    Job, Exposure, Camera, QA, Process, Configuration
)

def jsonify(data):
    ''' Make a dictionary with numpy arrays JSON serializable'''
    for key in data:
        if type(data[key]) == numpy.ndarray:
            data[key] = data[key].tolist()
    return data

def post(name, job_name, results, force=False):

    if name not in results:
        print('{} metric not found in {}'.format(name, results))

    qa = results[name]

    try:
        expid = qa['EXPID']
        arm = qa['ARM']
        spectrograph = qa['SPECTROGRAPH']
        paname = qa['PANAME']
        value = jsonify(qa['VALUE'])
    except:
        print("Fatal: unexpected format for QA file. Looking for 'EXPID', "
              "'ARM', 'SPECTROGRAPH', 'PANAME' and 'VALUE' keys.")
        sys.exit(1)

    # Make sure there is a configuration to refer to
    if not Configuration.objects.all():
        config_file = open('../qlf/static/ql.json', 'r')
        config_str = config_file.read()
        config_file.close()

        config_json = jsonify(json.loads(config_str))

        configuration = Configuration(configuration=config_json)
        configuration.save()

    configuration = Configuration.objects.latest('pk')

    camera = arm + str(spectrograph)

    # Check if camera is already registered
    if not Camera.objects.filter(camera=camera):
        camera_obj = Camera(camera=camera, arm=arm, spectrograph=spectrograph)
        camera_obj.save()
        print("Registered camera {}".format(camera_obj))

    # Save Job for this camera
    camera_obj = Camera.objects.get(camera=camera)

    # Check if expid is already registered
    if not Exposure.objects.filter(expid=expid):
        exposure = Exposure(expid=expid)
        exposure.save()
        print("Registered exposure {}".format(expid))

    # Save Process for this exposure
    exposure = Exposure.objects.get(expid=expid)

    if not Process.objects.filter(exposure_id=expid):
        process = Process(exposure_id=expid, configuration_id=configuration.id)
        process.save()

    # Save Job for this process
    process = Process.objects.get(exposure_id=expid)

    # Check if Job with name is already registered
    if not Job.objects.filter(name=job_name):
        job = Job(
            process_id=process.id,
            camera_id=camera_obj.camera, name=job_name
        )
        job.save()

    # Save QA Results for this job
    job = Job.objects.get(name=job_name)

    if not QA.objects.filter(name=name):
        # Register for QA results for the first time
        qa = QA(
            name=name, description='',
            paname=paname, metric=value, job_id=job.id
        )
        qa.save()
        print("Saved {} results for exposure={} and camera={}".format(name, expid, camera))
        print("See {}".format(QLF_API_URL))
    elif QA.objects.filter(name=name) and force:
        # Overwrite QA results
        QA.objects.filter(name=name).update(job_id=job.id, description='',
                                            paname=paname, metric=value)
        print("Overwritten {} results for exposure={} and camera={}".format(name, expid, camera))
    else:
        print("{} results for exposure={} and camera={} already "
              "registered. Use --force to overwrite.".format(name, expid, camera))


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

    post(qa_name, job_name, results, force)


