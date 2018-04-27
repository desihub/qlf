from rest_framework.test import APITestCase
from dashboard.models import Exposure
from rest_framework import status

class CustomerTest(APITestCase):

    def setUp(self):

        self.exposure = Exposure.objects.create(exposure_id=3, tile=6, telra=333.22, teldec=14.84, dateobs="2019-01-01T22:00:00Z", exptime=1000.0, flavor="science", night="20190101", airmass=None,)


    def test_get_customer(self):
        """                                                                                                                                                                                                                              
            Ensure we can get a exposure from db through the API                                                                                                                                                                             
        """
        response = self.client.get('/dashboard/api/exposure/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['exposure_id'], 3)
        self.assertEqual(response.data['results'][0]['tile'], 6)
