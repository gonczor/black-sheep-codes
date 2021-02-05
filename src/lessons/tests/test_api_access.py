from typing import Callable, Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from parameterized import parameterized
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from courses.models import CourseSignup, Course, CourseSection
from lessons.models import BaseLesson, Lesson
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
        CourseSignup.objects.create(course=self.course, user=self.user)

    def test_list_unauthenticated(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_authenticated(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @parameterized.expand(
        [
            ("get",),
            ("post",),
            ("patch",),
            ("delete",),
        ]
    )
    def test_lesson_actions_unauthenticated(self, action: str):
        response = self._get_response(action)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @parameterized.expand(
        [
            (None, "get", status.HTTP_200_OK),
            (None, "post", status.HTTP_403_FORBIDDEN),
            ("add_baselesson", "post", status.HTTP_201_CREATED),
            (None, "patch", status.HTTP_403_FORBIDDEN),
            ("change_baselesson", "patch", status.HTTP_200_OK),
            (None, "delete", status.HTTP_403_FORBIDDEN),
            ("delete_baselesson", "delete", status.HTTP_204_NO_CONTENT),
        ]
    )
    def test_lesson_actions(self, permission_name: Optional[str], action: str, status_code: int):
        self._assign_permission(permission_name)
        self.client.force_authenticate(self.user)

        response = self._get_response(action)

        self.assertEqual(response.status_code, status_code)

    def test_access_to_unsubscribed_lesson(self):
        unsubscribed_lesson = self._make_unsubscribed_course_lesson()
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.list_url)

        lesson_ids = [lesson["id"] for lesson in response.json()["results"]]
        self.assertIn(self.lesson.id, lesson_ids)
        self.assertNotIn(unsubscribed_lesson.id, lesson_ids)

    def test_access_to_unsubscribed_lesson_by_staff(self):
        unsubscribed_lesson = self._make_unsubscribed_course_lesson()
        self.user.is_staff = True
        self.user.save()
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.list_url)

        lesson_ids = [lesson["id"] for lesson in response.json()["results"]]
        self.assertIn(unsubscribed_lesson.id, lesson_ids)

    def test_access_to_unsubscribed_lesson_by_superuser(self):
        unsubscribed_lesson = self._make_unsubscribed_course_lesson()
        self.user.is_superuser = True
        self.user.save()
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.list_url)

        lesson_ids = [lesson["id"] for lesson in response.json()["results"]]
        self.assertIn(unsubscribed_lesson.id, lesson_ids)

    def _make_unsubscribed_course_lesson(self) -> Lesson:
        unsubscribed_course = Course.objects.create(name="unsubscribed")
        unsubscribed_section = CourseSection.objects.create(
            course=unsubscribed_course, name="unsubscribed"
        )
        return Lesson.objects.create(
            course_section=unsubscribed_section, name="unsubscribed"
        )

    def _assign_permission(self, permission_name: Optional[str]):
        if permission_name is None:
            return
        permissions = Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(BaseLesson), codename=permission_name
        )
        self.user.user_permissions.set(permissions)

    def _get_response(self, action: str) -> Response:
        if action in {"get", "post"}:
            url = self.list_url
        else:
            url = self.lesson_detail_url

        if action in {"get", "delete"}:
            data = None
        else:
            data = {
                "lesson_type": "Lesson",
                "name": "test lesson",
                "course_section": self.course_section.id,
            }

        method = self._get_method(action)

        return method(path=url, data=data)

    def _get_method(self, action: str) -> Callable:
        return getattr(self.client, action)
