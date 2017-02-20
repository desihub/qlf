import os
import sys
import argparse
import yaml
import numpy

QLF_API_URL = os.environ.get('QLF_API_URL',
                             'http://localhost:8000/dashboard/api')
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.append(os.path.join(BASE_DIR, "qlf"))

os.environ['DJANGO_SETTINGS_MODULE'] = 'qlf.settings'

from dashboard.models import Job, Exposure, Camera, QA

def jsonify(data):
    ''' Make a dictionary with numpy arrays JSON serializable'''
    for key in data:
        if type(data[key]) == numpy.ndarray:
            data[key] = data[key].tolist()
    return data

def post(name, results, force=False):

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

    # Make sure there is a job to refer to
    if not Job.objects.all():
        Job.objects.create()

    # Check if expid is already registered
    if not Exposure.objects.filter(expid=expid):
        job = Job.objects.latest('pk')
        exposure = Exposure(job=job, expid=expid)
        exposure.save()
        print("Registered exposure {}".format(expid))

    camera = arm + str(spectrograph)

    # Check if camera is already registered
    if not Camera.objects.filter(camera=camera):
        exposure = Exposure.objects.filter(expid=expid)[0]
        camera = Camera(camera=camera, exposure=exposure,
                        arm=arm, spectrograph=spectrograph)
        camera.save()
        print("Registered camera {}".format(camera))

    # Save QA results for this exposure and camera`
    camera = Camera.objects.filter(camera=camera)[0]

    if not QA.objects.filter(name=name):
        # Register for QA results for the first time
        qa = QA(camera=camera, name=name, description='', paname=paname, value=value)
        qa.save()
        print("Saved {} results for exposure={} and camera={}".format(name, expid, camera))
        print("See {}".format(QLF_API_URL))
    elif QA.objects.filter(name=name) and force:
        # Overwrite QA results
        QA.objects.filter(name=name).update(camera=camera, description='',
                                            paname=paname, value=value)
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
    results = yaml.load(open(file, 'r'))

    force = parser.parse_args().force

    post(qa_name, results, force)


