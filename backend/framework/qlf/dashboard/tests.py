from rest_framework.test import APITestCase
from dashboard.models import Exposure, Process, Job, Camera
from rest_framework import status
from unittest.mock import patch
import datetime


class ExposureTest(APITestCase):
    def setUp(self):
        self.exposure = Exposure.objects.create(
            exposure_id=3,
            tile=6,
            telra=333.22,
            teldec=14.84,
            dateobs="2019-01-01T22:00:00Z",
            exptime=1000.0,
            flavor="science",
            night="20190101",
            airmass=None,
        )
        self.exposure_two = Exposure.objects.create(
            exposure_id=7,
            tile=8,
            telra=332.22,
            teldec=15.84,
            dateobs="2019-01-01T22:00:00Z",
            exptime=1000.0,
            flavor="science",
            night="20190101",
            airmass=None,
        )

    def test_get_exposure(self):
        """Ensure we can get a exposure from db through the API"""
        response = self.client.get('/dashboard/api/exposure/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['exposure_id'], 3)
        self.assertEqual(response.data['results'][0]['tile'], 6)
        self.assertEqual(response.data['results'][1]['exposure_id'], 7)


class ProcessTest(APITestCase):
    def setUp(self):
        self.exposure = Exposure.objects.create(
            exposure_id=3,
            tile=6,
            telra=333.22,
            teldec=14.84,
            dateobs="2019-01-01T22:00:00Z",
            exptime=1000.0,
            flavor="science",
            night="20190101",
            airmass=None,
        )
        self.process = Process.objects.create(
            pk=7,
            pipeline_name="Quick Look",
            start="2018-04-26T20:06:28.563787Z",
            end="2018-04-26T20:07:59Z",
            status=0,
            version="",
            process_dir="exposures/20190101/00000003",
            exposure=self.exposure,
        )

    def test_get_process(self):
        """Ensure we can get a process from db through the API"""
        response = self.client.get('/dashboard/api/process/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['pk'], 7)
        self.assertEqual(response.data['results'][0]['exposure'], 3)


class CameraTest(APITestCase):
    def setUp(self):
        self.camera = Camera.objects.create(
            camera="b3",
            spectrograph="3",
            arm="b",
        )

    def test_get_camera(self):
        """Ensure we can get a camera from db through the API"""
        response = self.client.get('/dashboard/api/camera/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['camera'], 'b3')
        self.assertEqual(response.data['results'][0]['spectrograph'], '3')
        self.assertEqual(response.data['results'][0]['arm'], 'b')


class JobTest(APITestCase):
    def setUp(self):
        self.exposure = Exposure.objects.create(
            exposure_id=3,
            tile=6,
            telra=333.22,
            teldec=14.84,
            dateobs="2019-01-01T22:00:00Z",
            exptime=1000.0,
            flavor="science",
            night="20190101",
            airmass=None,
        )
        self.process = Process.objects.create(
            pk=7,
            pipeline_name="Quick Look",
            start="2018-04-26T20:06:28.563787Z",
            end="2018-04-26T20:07:59Z",
            status=0,
            version="",
            process_dir="exposures/20190101/00000003",
            exposure=self.exposure,
        )
        self.camera = Camera.objects.create(
            camera="b3",
            spectrograph="3",
            arm="b",
        )
        self.job = Job.objects.create(
            pk=7,
            name="Quick Look",
            start="2018-04-26T20:06:28.646376Z",
            end="2018-04-26T20:07:59Z",
            status=0,
            version="1.0",
            logname="exposures/20190101/00000003/run-b3.log",
            process=self.process,
            camera=self.camera,
        )

    def test_get_job(self):
        """Ensure we can get last process from db through the API"""
        response = self.client.get('/dashboard/api/job/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['process'], 7)
        self.assertEqual(response.data['results'][0]['camera'], 'b3')


def mock_pipeline(self):
        self.exposure = Exposure.objects.create(
            exposure_id=3,
            tile=6,
            telra=333.22,
            teldec=14.84,
            dateobs="2019-01-01T22:00:00Z",
            exptime=1000.0,
            flavor="science",
            night="20190101",
            airmass=None,
        )
        self.process = Process.objects.create(
            pk=8,
            pipeline_name="Quick Look",
            start="2018-04-26T20:06:28.563787Z",
            end="2018-04-26T20:07:59Z",
            status=0,
            version="",
            process_dir="exposures/20190101/00000003",
            exposure=self.exposure,
        )
        self.camera = Camera.objects.create(
            camera="b3",
            spectrograph="3",
            arm="b",
        )
        self.job = Job.objects.create(
            pk=7,
            name="Quick Look",
            start="2018-04-26T20:06:28.646376Z",
            end="2018-04-26T20:07:59Z",
            status=0,
            version="1.0",
            logname="exposures/20190101/00000003/run-b3.log",
            process=self.process,
            camera=self.camera,
        )

        return self


class LastProcessTest(APITestCase):
    def setUp(self):
        mock_pipeline(self)

    def test_get_last_process(self):
        """Ensure we can get last process from db through the API"""
        response = self.client.get('/dashboard/api/last_process/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['id'], 8)
        self.assertEqual(response.data[0]['exposure'], 3)
        self.assertEqual(response.data[0]['process_jobs'][0]['pk'], 7)


class ProcessingHistoryTest(APITestCase):
    def setUp(self):
        mock_pipeline(self)

    def test_get_processing_history(self):
        """Ensure we can get processing_history from db through the API"""
        response = self.client.get('/dashboard/api/processing_history/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['pk'], 8)
        self.assertIsNotNone(response.data['results']
                             [0]['exposure']['dateobs'])
        self.assertEqual(response.data['results'][0]['datemjd'], None)
        self.assertEqual(response.data['results']
                         [0]['exposure']['exposure_id'], 3)
        self.assertEqual(response.data['results'][0]['exposure']['tile'], 6)
        self.assertEqual(response.data['results']
                         [0]['exposure']['telra'], 333.22)
        self.assertEqual(response.data['results']
                         [0]['exposure']['teldec'], 14.84)
        self.assertEqual(response.data['results']
                         [0]['exposure']['exptime'], 1000.0)
        self.assertEqual(response.data['results']
                         [0]['exposure']['airmass'], None)
        self.assertEqual(response.data['results']
                         [0]['exposure']['flavor'], "science")
        self.assertIsNotNone(response.data['results'][0]['runtime'])
        self.assertIsNotNone(response.data['results'][0]['start'])
        self.assertIsNotNone(response.data['results'][0]['end'])


class ObservingHistoryTest(APITestCase):
    def setUp(self):
        mock_pipeline(self)

    def test_get_observing_history(self):
        """Ensure we can get observing_history from db through the API"""
        response = self.client.get('/dashboard/api/observing_history/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['results']
                             [0]['dateobs'])
        self.assertEqual(response.data['results'][0]['datemjd'], None)
        self.assertEqual(response.data['results'][0]['exposure_id'], 3)
        self.assertEqual(response.data['results'][0]['tile'], 6)
        self.assertEqual(response.data['results'][0]['telra'], 333.22)
        self.assertEqual(response.data['results'][0]['teldec'], 14.84)
        self.assertEqual(response.data['results'][0]['exptime'], 1000.0)
        self.assertEqual(response.data['results'][0]['airmass'], None)
