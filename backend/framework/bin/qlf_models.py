import os
import sys
import yaml
import glob
import json
import numpy
import django
import math
import logging

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.append(os.path.join(BASE_DIR, "qlf"))

os.environ['DJANGO_SETTINGS_MODULE'] = 'qlf.settings'

django.setup()

from django import db
from dashboard.models import (
    Job, Exposure, Camera, QA, Process, Configuration
)

logger = logging.getLogger()


class QLFModels(object):
    """ Class responsible by manage the database models from Quick Look pipeline. """

    def __init__(self):
        """ Due to the continuous processing of exposures and consequently the long
        waiting period of Django's ORM. Whenever instantiated, the connection
        is closed to be recreated when requested. """

        db.connection.close()

    def insert_exposure(
            self, expid, night, telra=None, teldec=None,
            tile=None, dateobs=None, flavor=None, exptime=None
    ):
        """ Inserts and gets exposure and night if necessary. """

        # Check if expid is already registered
        if not Exposure.objects.filter(exposure_id=expid):
            exposure = Exposure(
                exposure_id=expid, night=night,
                telra=telra, teldec=teldec,
                tile=tile, dateobs=dateobs,
                flavor=flavor, exptime=exptime
            )
            exposure.save()

        # Save Process for this exposure
        return Exposure.objects.get(exposure_id=expid)

    def insert_process(self, data, pipeline_name):
        """ Inserts initial data in process table. """

        exposure = self.insert_exposure(
            data.get('expid'),
            data.get('night'),
            data.get('telra', None),
            data.get('teldec', None),
            data.get('tile', None),
            data.get('dateobs', None),
            data.get('flavor', None),
            data.get('exptime', None)
        )

        process = Process(
            exposure_id=exposure.exposure_id,
            start=data.get('start'),
            pipeline_name=pipeline_name
        )

        process.save()

        return process

    def insert_config(self, process_id):
        """ Inserts used configuration. """

        # TODO: get configuration coming of interface
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

    def update_process(self, process_id, end, process_dir, status):
        """ Updates process with execution results. """

        process = Process.objects.filter(id=process_id).update(
            end=end,
            process_dir=process_dir,
            status=status
        )

        return process

    def update_job(self, job_id, end, status, output_path):
        """ Updates job with execution results. """

        # Close the DB connections
        django.db.connection.close()

        try:
            Job.objects.filter(id=job_id).update(
                end=end,
                status=status
            )

            qas = list()

            for product in glob.glob(output_path):
                qa = self.create_qa_bulk(product, job_id)
                if not qa:
                    logger.warning('Error to create QA: {}'.format(product))
                    continue

                qas.append(qa)

            QA.objects.bulk_create(qas)

            logger.info('Job {} updated.'.format(job_id))
        except Exception as err:
            logger.error('Job {} failed.'.format(job_id))
            logger.error(err)

    def create_qa_bulk(self, product, job_id):
        """ Creates QAs in bulk """

        qa = yaml.load(open(product, 'r'))
        name = os.path.basename(product)

        for item in ('PANAME', 'METRICS', 'PARAMS'):
            if item not in qa:
                logger.warning('{} not found.'.format(item))
                return None

        paname = qa['PANAME']
        metrics = self.jsonify(qa['METRICS'])
        params = self.jsonify(qa['PARAMS'])

        return QA(
            name=name,
            description='',
            paname=paname,
            metrics=metrics,
            params=params,
            job_id=job_id
        )

    def update_qa_tests(self, name, qa_tests):
        """ Update QA tests """

        Camera.objects.filter(camera=name).update(
            qa_tests=qa_tests
        )

    def insert_qa(self, name, paname, metrics, params, job_id, force=False):
        """ Inserts table """

        # Register for QA results for the first time
        qa = QA(
            name=name,
            description='',
            paname=paname,
            metrics=metrics,
            params=params,
            job_id=job_id
        )
        qa.save()

    def get_qa(self, process_id, cam, qa_name):
        """ Gets QA """
        try:
            qa = Process.objects.get(pk=process_id).process_jobs.get(camera_id=cam).job_qas.get(name=qa_name)
        except QA.DoesNotExist:
            qa = None

        return qa

    def get_process_by_process_id(self, process_id):
        """ Gets Process using process_id"""
        try:
            process = Process.objects.get(pk=process_id)
        except Process.DoesNotExist:
            process = None

        return process

    def get_cameras(self):
        """ Gets cameras """

        return Camera.objects.all()

    def get_jobs_by_process_id(self, process_id):
        """ get cameras by job id """

        jobs = list()
        for job in Job.objects.filter(process=process_id):
            jobs.append(job)
        return jobs

    def get_expid_in_process(self, expid):
        """ Gets process object by expid """

        return Process.objects.filter(exposure_id=expid)

    def get_last_exposure(self):
        """ Gets last processed exposures """

        try:
            exposure = Exposure.objects.latest('pk')
        except Exposure.DoesNotExist:
            exposure = None

        return exposure

    def get_job(self, job_id):
        """ gets last processed exposures """

        try:
            exposure = Job.objects.filter(id=job_id)
        except:
            exposure = None

        return exposure

    def delete_all_processes(self):
        """ Delete all processes """

        Process.objects.all().delete()

    def delete_all_exposures(self):
        """ Delete all exposures """

        Exposure.objects.all().delete()

    def delete_all_cameras(self):
        """ Delete all cameras """

        Camera.objects.all().delete()

    def delete_process(self, process_id):
        """ Delete by process_id """

        Process.objects.filter(id=process_id).delete()

    def delete_exposure(self, expid):
        """ Delete by exposure id """

        Exposure.objects.filter(exposure_id=expid).delete()

    @staticmethod
    def jsonify(data):
        """ Make a dictionary with numpy arrays JSON serializable """

        for key in data:
            if type(data[key]) == numpy.ndarray:
                data[key] = data[key].tolist()

            if isinstance(data[key], list):
                data[key] = [0 if isinstance(x, float) and math.isnan(x) else x for x in data[key]]

        return data


if __name__ == '__main__':
    qlf = QLFModels()
