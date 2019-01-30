import glob
import json
import logging
import math
import os
import sys
from datetime import datetime, timedelta

import django
import numpy

qlf_root = os.environ.get('QLF_ROOT')

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.append(os.path.join(BASE_DIR, "qlf"))

os.environ['DJANGO_SETTINGS_MODULE'] = 'qlf.settings'

django.setup()

from dashboard.models import (
    Camera, Configuration, Exposure, Job, Process, Fibermap, Product
)
from django.db.models import F
from astropy.time import Time

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

    def insert_fibermap(self, **kwargs):
        exposure = kwargs.get('exposure')

        # Check if fibermap is already registered
        if not Fibermap.objects.filter(exposure=exposure):
            fibermap = Fibermap(
                exposure=exposure,
                fiber_ra=kwargs.get('fiber_ra'),
                fiber_dec=kwargs.get('fiber_dec'),
                fiber=kwargs.get('fiber'),
                objtype=kwargs.get('objtype')
            )
            fibermap.save()

        # Save Process for this exposure
        return Fibermap.objects.get(exposure=exposure)

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

            self.create_products(job_id)

            logger.info('Job {} updated.'.format(job_id))
        except Exception as err:
            logger.error('Job {} failed.'.format(job_id))
            logger.error(err)

    def create_products(self, job_id):
        metrics_path = os.path.join(
            qlf_root, "framework", "ql_mapping",
            "metrics.json")

        with open(metrics_path) as f:
            metrics = json.load(f)

        query = Job.objects.filter(id=job_id)
        values = {}
        for key in metrics:
            output_path = 'output'
            path_keys = metrics[key]['path']
            for path_key in path_keys.split('->'):
                output_path += "->'{}'".format(path_key)
            values[key] = output_path

        job = query.extra(
            select=values
        ).annotate(
            dateobs=F("process__exposure__dateobs")
        ).values(*list(values), "dateobs", 'id').last()

        for key in metrics:
            date_time = (job['dateobs']).strftime('%Y-%m-%d %H:%M:%S')
            value = []
            if isinstance(job[key], list):
                value = job[key]
            else:
                value = [job[key]]
            mjd = Time(date_time, format='iso', scale='utc').mjd
            p = Product(
                job_id=job_id,
                value=value,
                key=key,
                mjd=mjd
            )
            p.save()

    def get_last_configuration(self):
        return Configuration.objects.latest('pk')


    def get_output(self, process_id, cam):
        """ Gets QA """
        try:
            obj = Job.objects.filter(process_id=process_id).get(camera=cam)
            qa = obj.output
        except Job.DoesNotExist:
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

    def get_flavors(self):
        """ Get all flavors
        """

        return Exposure.objects.values_list('flavor', flat=True).distinct()


    def get_last_exposure(self):
        """ Gets last processed exposures """

        try:
            exposure = Exposure.objects.latest('pk')
        except Exposure.DoesNotExist:
            exposure = None

        return exposure

    def get_last_exposure_by_program(self, program):
        """ Get last processed exposures by program """

        try:
            exposure = Exposure.objects.filter(process_exposure__isnull=False)
            exposure = exposure.filter(program=program).latest('pk')
        except Exposure.DoesNotExist:
            exposure = None

        return exposure

    def get_last_exposure_by_flavor(self, flavor):
        """ Get last processed exposures by flavor """

        try:
            exposure = Exposure.objects.filter(process_exposure__isnull=False)
            exposure = exposure.filter(flavor=flavor).latest('pk')
        except Exposure.DoesNotExist:
            exposure = None

        return exposure

    def get_last_fibermap_by_flavor(self, flavor):
        """ Get last processed exposures by flavor """

        try:
            exposure = self.get_last_exposure_by_flavor(flavor)
            fibermap = Fibermap.objects.filter(exposure=exposure).latest('pk')
        except Exposure.DoesNotExist:
            fibermap = None

        return fibermap

    def get_last_process_by_flavor(self, flavor, jobs_isnull=True):
        """Get last process by flavor
        
        Arguments:
            flavor {str} -- flavor exposure
        """

        try:
            process = Process.objects.filter(
                exposure__flavor=flavor
            ).filter(
                process_jobs__isnull=jobs_isnull
            ).latest('exposure__flavor')
        except Process.DoesNotExist:
            process = None

        return process

    def get_last_process_by_exposure_id(self, exposure_id, has_jobs=False):
        """Get last process by exposure_id
        
        Arguments:
            exposure_id {str} -- exposure ID
        """

        try:
            process = Process.objects.filter(
                exposure_id=exposure_id
            )
            
            if has_jobs:
                process = process.filter(process_jobs__isnull=False)

            process = process.latest('exposure_id')
        except Process.DoesNotExist:
            process = None

        return process

    def get_job(self, job_id):
        """ Get last processed exposures """

        try:
            exposure = Job.objects.filter(id=job_id)
        except:
            exposure = None

        return exposure

    def get_outputs_json_chunk_by_camera(self, path_keys, camera, begin_date=None, end_date=None):
        """ Obtains specific chunk of QA outputs by camera from the database.
        
        Arguments:
            path_keys {str} -- path to specific QA outputs
                e.g.: "GENERAL_INFO->B_PEAKS"
            camera {str} -- selected camera
        
        Keyword Arguments:
            begin_date {str} -- obtains entries beginning this date (default: None)
            end_date {str} -- obtains entries until this date (default: None)
        """

        jobs_obj = Job.objects.filter(camera=camera)

        if begin_date:
            begin_date = datetime.strptime(begin_date, "%Y-%m-%d")
            jobs_obj = jobs_obj.filter(process__exposure__dateobs__gte=begin_date)
            
        if end_date:
            end_date = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
            jobs_obj = jobs_obj.filter(process__exposure__dateobs__lte=end_date)

        output_path = 'output'

        for key in path_keys.split('->'):
            output_path += "->'{}'".format(key)

        outputs = jobs_obj.extra(
            select={"value": output_path}
        ).annotate(
            exposure_id=F("process__exposure__exposure_id"),
            dateobs=F("process__exposure__dateobs")
        ).values(
            "camera", "exposure_id", "dateobs", "value"
        ).distinct().order_by('dateobs')

        return outputs

    def migrate_outputs(self, metrics):
        Product.objects.all().delete()
        query=Job.objects.all()
        values = {}
        for key in metrics:
            output_path = 'output'
            path_keys = metrics[key]['path']
            for path_key in path_keys.split('->'):
                output_path += "->'{}'".format(path_key)
            values[key] = output_path

        query = query.extra(
            select=values
        ).annotate(
            dateobs=F("process__exposure__dateobs")
        ).values(*list(values), "dateobs", 'id')

        step=500
        start=0
        end=step
        jobs = query[start:end]

        while len(jobs) is not 0:
            print('Ingesting: {} - {}'.format(start, end))
            for job in jobs:
                for key in metrics:
                    date_time=(job['dateobs']).strftime('%Y-%m-%d %H:%M:%S')
                    value = []
                    if isinstance(job[key], list):
                        value = job[key]
                    else:
                        value = [job[key]]
                    mjd=Time(date_time, format='iso', scale='utc').mjd
                    p = Product(
                        job_id=job['id'],
                        value=value,
                        key=key,
                        mjd=mjd
                    )
                    p.save()
            start = start + step
            end = end + step
            jobs = query[start:end]


    def get_product_metrics_by_camera(self, key, camera, begin_date=None, end_date=None):
        vals = Product.objects.filter(job__camera=camera, key=key)
        if begin_date:
            begin_date = datetime.strptime(begin_date, "%Y-%m-%d")
            vals = vals.filter(job__process__exposure__dateobs__gte=begin_date)
            
        if end_date:
            end_date = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
            vals = vals.filter(job__process__exposure__dateobs__lte=end_date)

        output = vals.extra(
            select={
                'datef':"to_char(dateobs, 'YYYY-MM-DD HH24:MI:SS')"
            }
        ).annotate(
            camera=F("job__camera"),
            exposure_id=F("job__process__exposure__exposure_id"),
            dateobs=F("job__process__exposure__dateobs")
        ).values("camera", "exposure_id", "dateobs", "value", "datef", "mjd").distinct().order_by('dateobs')
        return output

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
