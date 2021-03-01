from django.contrib.auth import get_user_model
from parameterized import parameterized
from rest_framework import status
from rest_framework.test import APITestCase


class AuthenticationTestCAse(APITestCase):
    def test_create_account_with_blank_email(self):
        data = {
            "username": "test",
            "email": "",
            "password": "Test123",
            "re_password": "Test123",
        }
        url = "/api/v1/auth/users/"

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"email": ["This field may not be blank."]})


class AccessToOwnDataTestCase(APITestCase):
    def setUp(self):
        self.user_password = "test"
        self.User = get_user_model()
        self.user = self.User.objects.create_user(
            username="test", email="test@example.com", password=self.user_password
        )
        self.client.force_authenticate(user=self.user)

    @parameterized.expand(
        [
            ("/api/v1/auth/users/",),
            ("/api/v1/auth/users/me/",),
        ]
    )
    def test_delete_own(self, endpoint: str):
        response = self.client.delete(
            path=self._get_url(path=endpoint, user_id=self.user.id),
            data={"current_password": self.user_password},
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @parameterized.expand(
        [
            ("/api/v1/auth/users/",),
            ("/api/v1/auth/users/me/",),
        ]
    )
    def test_update_own_username(self, endpoint: str):
        response = self.client.patch(
            path=self._get_url(path=endpoint, user_id=self.user.id),
            data={"username": "NewUsername"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @parameterized.expand(
        [
            ("/api/v1/auth/users/",),
            ("/api/v1/auth/users/me/",),
        ]
    )
    def test_update_own_email(self, endpoint: str):
        response = self.client.patch(
            path=self._get_url(path=endpoint, user_id=self.user.id),
            data={"email": "new@example.com"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @parameterized.expand(
        [
            ("/api/v1/auth/users/",),
            ("/api/v1/auth/users/me/",),
        ]
    )
    def test_retrieve_own(self, endpoint: str):
        response = self.client.get(
            path=self._get_url(path=endpoint, user_id=self.user.id),
            data={"email": "new@example.com"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_other_user(self):
        other_user = self.User.objects.create_user(
            username="other", email="test2@example.com", password=self.user_password
        )
        response = self.client.delete(
            path=self._get_url(path="/api/v1/auth/users/", user_id=other_user.id),
            data={"current_password": self.user_password},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_other_user_username(self):
        other_user = self.User.objects.create_user(
            username="other", email="test2@example.com", password=self.user_password
        )
        response = self.client.patch(
            path=self._get_url(path="/api/v1/auth/users/", user_id=other_user.id),
            data={"username": "NewUsername"},
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_other_user(self):
        other_user = self.User.objects.create_user(
            username="other", email="test2@example.com", password=self.user_password
        )
        response = self.client.get(
            path=self._get_url(path="/api/v1/auth/users/", user_id=other_user.id),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def _get_url(self, path: str, user_id: int = None) -> str:
        if "me" in path or user_id is None:
            return path
        else:
            return f"{path}{user_id}/"
