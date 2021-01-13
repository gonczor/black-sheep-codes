from rest_framework.test import APITestCase


class MyTestCase(APITestCase):
    def test_something(self):
        self.assertEqual(2+2, 4)
