from rest_framework import status
from rest_framework.test import APITestCase


class AuthenticationTestCAse(APITestCase):
    def test_create_account_with_blank_email(self):
        data = {
            'username': 'test',
            'email': '',
            'password': 'Test123',
            're_password': 'Test123'
        }
        url = '/api/v1/auth/users/'

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'email': ['This field may not be blank.']})
