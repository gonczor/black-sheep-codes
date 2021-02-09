from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from courses.models import CourseSignup
from lessons.tests import BaseLessonTestCase


class LessonAPITestCase(BaseLessonTestCase, APITestCase):
    def setUp(self):
        super().setUp()
        self.mark_as_complete_url = reverse(
            "lessons:lesson-mark_as_complete", args=(self.lesson.id,)
        )
        self.revert_mark_as_complete_url = reverse(
            "lessons:lesson-revert_mark_as_complete", args=(self.lesson.id,)
        )
        User = get_user_model()
        self.user = User.objects.create_user(
            username="test", email="test@example.com", password="test"
        )
        CourseSignup.objects.create(course=self.course, user=self.user)

    def test_mark_as_complete(self):
        self.client.force_authenticate(self.user)

        response = self.client.patch(self.mark_as_complete_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(self.lesson.is_completed_by(self.user))

    def test_revert_mark_as_complete(self):
        self.client.force_authenticate(self.user)

        response = self.client.patch(self.revert_mark_as_complete_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.lesson.is_completed_by(self.user))

    def test_mark_as_complete_duplicate(self):
        self.client.force_authenticate(self.user)
        self.lesson.complete(self.user)

        response = self.client.patch(self.mark_as_complete_url)

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
