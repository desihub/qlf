import os
import argparse
import yaml
import numpy
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qlf.settings")

from dashboard.models import Job, Exposure, Camera, QA


def jsonify(data):
    ''' Make a dictionary with numpy arrays JSON serializable'''
    for key in data:
        if type(data[key]) == numpy.ndarray:
            data[key] = data[key].tolist()
    return data

def post(name, results):

    if name not in results:
        print('{} metric not found in {}'.format(name, results))

    qa = results[name]

    expid = qa['EXPID']
    arm = qa['ARM']
    spectrograph = qa['SPECTROGRAPH']
    paname = qa['PANAME']
    value = jsonify(qa['VALUE'])

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

    # Save QA results for this camera
    camera = Camera.objects.filter(camera=camera)[0]
    qa = QA(camera=camera, name=name, description='some', paname=paname, value=value)
    qa.save()

    print("Saved {} results for exposure={} and camera={}".format(name, expid, camera))


if __name__=='__main__':

    parser = argparse.ArgumentParser(
        description="""Upload QA metrics produced by the Quick Look pipeline to QLF database.
This script is meant to be run from command line for testing or imported by Quick Look. """,
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

    qa_name = parser.parse_args().qa_name

    file = parser.parse_args().file
    results = yaml.load(open(file, 'r'))

    post(qa_name, results)


