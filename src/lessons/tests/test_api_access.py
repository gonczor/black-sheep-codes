from typing import Callable, Optional

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from parameterized import parameterized
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase

from courses.models import Course, CourseSection, CourseSignup
from lessons.models import BaseLesson, Comment, Lesson
from lessons.tests import BaseCommentTestCase, BaseLessonTestCase


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
        return Lesson.objects.create(course_section=unsubscribed_section, name="unsubscribed")

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


class CommentsApiTestCase(BaseCommentTestCase, APITestCase):
    def test_unauthenticated_access_to_list(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_access_to_detail(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_view_list(self):
        self.client.force_authenticate(user=self.author)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_view_detail(self):
        self.client.force_authenticate(user=self.author)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_create(self):
        data = {"lesson": self.lesson.pk, "text": "Something"}
        self.client.force_authenticate(user=self.author)
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @parameterized.expand([("put",), ("patch",), ("delete",)])
    def test_actions_on_own(self, action: str):
        data = {"text": "Something"}
        self.client.force_authenticate(user=self.author)
        response = self._make_request(action=action, data=data)
        if action == "delete":
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        else:
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    @parameterized.expand([("put",), ("patch",), ("delete",)])
    def test_can_not_perform_actions_someones_comment(self, action):
        User = get_user_model()
        new_author = User.objects.create_user(
            username="test1", email="test1@example.com", password="test"
        )
        data = {"text": "Something"}
        self.client.force_authenticate(user=new_author)
        response = self._make_request(action=action, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.comment.refresh_from_db()
        self.assertNotEqual(self.comment.text, "Something")

    @parameterized.expand([("put",), ("patch",), ("delete",)])
    def test_can_update_someones_comment_with_permission_assigned(self, action):
        User = get_user_model()
        moderator = User.objects.create_user(
            username="test1", email="test1@example.com", password="test"
        )
        permissions = Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(Comment),
            codename__in=("change_comment", "soft_delete_comment"),
        )
        moderator.user_permissions.set(permissions)
        data = {"text": "Something"}
        self.client.force_authenticate(user=moderator)
        response = self._make_request(action, data)
        if action == "delete":
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        else:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.comment.refresh_from_db()
            self.assertEqual(self.comment.text, "Something")

    def _make_request(self, action: str, data: dict):
        method = self._get_method(action)

        return method(path=self.detail_url, data=data)

    def _get_method(self, action: str) -> Callable:
        return getattr(self.client, action)
