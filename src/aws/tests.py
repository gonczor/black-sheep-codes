from django.test import TestCase
from rest_framework import status


class HealthViewTestCase(TestCase):
    def test_request(self):
        response = self.client.get("/health/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
