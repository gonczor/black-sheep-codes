from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lessons.tests import BaseLessonTestCase


class LessonAPITestCase(BaseLessonTestCase, APITestCase):
    def setUp(self):
        super().setUp()
        self.list_url = reverse("lessons:lesson-list")
        self.lesson_detail_url = reverse("lessons:lesson-detail", args=(self.lesson.id,))
        User = get_user_model()
        self.user = User.objects.create_user(
            username="test", email="test@example.com", password="test"
        )

    def test_list_unauthenticated(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_authenticated(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
