import glob
import json
import logging
import math
import os
import sys

import django
import numpy

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.append(os.path.join(BASE_DIR, "qlf"))

os.environ['DJANGO_SETTINGS_MODULE'] = 'qlf.settings'

django.setup()

from dashboard.models import (
    QA, Camera, Configuration, Exposure, Job, Process
)

logger = logging.getLogger()


class QLFModels(object):
    """ Class responsible by manage the database models from
    Quick Look pipeline. """

    def __init__(self):
        """ Due to the continuous processing of exposures and consequently the long
        waiting period of Django's ORM. Whenever instantiated, the connection
        is closed to be recreated when requested. """

        django.db.connection.close()

    def insert_exposure(self, **kwargs):
        """ Inserts and gets exposure and night if necessary. """

        exposure_id = kwargs.get('exposure_id')

        # Check if exposure_id is already registered
        if not Exposure.objects.filter(exposure_id=exposure_id):
            exposure = Exposure(
                exposure_id=kwargs.get('exposure_id'),
                night=kwargs.get('night'),
                telra=kwargs.get('telra'),
                teldec=kwargs.get('teldec'),
                tile=kwargs.get('tile'),
                dateobs=kwargs.get('dateobs'),
                flavor=kwargs.get('flavor'),
                program=kwargs.get('program', None),
                airmass=kwargs.get('airmass', None),
                exptime=kwargs.get('exptime', None)
            )
            exposure.save()

        # Save Process for this exposure
        return Exposure.objects.get(exposure_id=exposure_id)

    def insert_process(self, data, pipeline_name):
        """ Inserts initial data in process table. """

        exposure = self.insert_exposure(**data)

        process = Process(
            exposure_id=exposure.exposure_id,
            start=data.get('start'),
            pipeline_name=pipeline_name
        )

        process.save()

        return process

    def insert_config(self, name, default_configuration):
        """ Inserts used configuration. """

        # TODO: get configuration coming of interface
        # Make sure there is a configuration to refer to

        try:
            configuration = Configuration.objects.get(name=name)
        except Configuration.DoesNotExist:
            configuration = Configuration(
                name=name,
                configuration=default_configuration,
            )
            configuration.save()

        return Configuration.objects.get(name=name)

    def insert_camera(self, camera):
        """ Inserts used camera. """

        # Check if camera is already registered
        try:
            camera_obj = Camera.objects.get(camera=camera)
        except Camera.DoesNotExist:
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

    def update_process(self, process_id, end, process_dir, status, qa_tests):
        """ Updates process with execution results. """

        process = Process.objects.filter(id=process_id).update(
            end=end,
            process_dir=process_dir,
            status=status,
            qa_tests=qa_tests
        )

        return process

    def abort_current_process(self):
        try:
            process = Process.objects.latest('pk')
            if process.process_jobs.last().status == 2:
                for job in process.process_jobs.all():
                    job.status = 1
                    job.save()
            else:
                return
        except Process.DoesNotExist as error:
            logger.debug(error)

    def update_job(self, job_id, exposure_id, camera, end, status, output_path):
        """ Updates job with execution results. """

        # Close the DB connections
        django.db.connection.close()

        merged_path = os.path.join(
            output_path, 'ql-mergedQA-%s-%s.json' % (
                camera,
                str(exposure_id).zfill(8)
            )
        )

        ql_merged = {}

        if os.path.isfile(merged_path):
            with open(merged_path, 'r') as merged_file:
                ql_merged = jsonify(json.load(merged_file))
                merged_file.close()

        try:
            Job.objects.filter(id=job_id).update(
                end=end,
                output=ql_merged,
                status=status
            )

            qas = list()

            output_path = os.path.join(
                output_path, 'ql-*-%s-%s.json' % (
                    camera,
                    str(exposure_id).zfill(8)
                )
            )

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

        with open(product, 'r') as product_file:
            qa = json.load(product_file)
            product_file.close()

        name = os.path.basename(product)

        for item in ('PANAME', 'METRICS', 'PARAMS'):
            if item not in qa:
                logger.warning('{} not found.'.format(item))
                return None

        paname = qa['PANAME']
        metrics = jsonify(qa['METRICS'])
        params = jsonify(qa['PARAMS'])

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

    def get_last_configuration(self):
        return Configuration.objects.latest('pk')

    def get_qa(self, process_id, cam, qa_name):
        """ Gets QA """
        try:
            qa = Process.objects.get(pk=process_id).process_jobs.get(
                camera_id=cam).job_qas.get(name=qa_name)
        except QA.DoesNotExist:
            qa = None

        return qa

    def get_merged_qa(self, process_id, cam):
        """ Gets QA """
        try:
            qa = Process.objects.get(pk=process_id).process_jobs.get(
                camera_id=cam).output
        except QA.DoesNotExist:
            qa = None

        return qa

    def get_output(self, process_id, cam):
        """ Gets QA """
        try:
            obj = Job.objects.filter(process_id=process_id).get(camera=cam)
            qa = obj.output
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

    def get_expid_in_process(self, exposure_id):
        """ Gets process object by exposure_id """

        return Process.objects.filter(exposure_id=exposure_id)

    def get_last_exposure(self):
        """ Gets last processed exposures """

        try:
            exposure = Exposure.objects.latest('pk')
        except Exposure.DoesNotExist:
            exposure = None

        return exposure

    def get_last_exposure_by_program(self, program):
        """ Gets last processed exposures by program """

        try:
            exposure = Exposure.objects.filter(process_exposure__isnull=False)
            exposure = exposure.filter(program=program).latest('pk')
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

    def delete_exposure(self, exposure_id):
        """ Delete by exposure id """

        Exposure.objects.filter(exposure_id=exposure_id).delete()


def jsonify(data):
    """ Make a dictionary with numpy arrays JSON serializable """
    if type(data) == numpy.ndarray:
        data = data.tolist()
    if isinstance(data, list):
        for item in data:
            data[data.index(item)] = jsonify(item)
    if isinstance(data, dict):
        for item in data:
            data[item] = jsonify(data[item])
    if isinstance(data, float):
        if math.isnan(data) or math.isinf(data):
            data = -9999
    return data


if __name__ == '__main__':
    qlf = QLFModels()
