from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import signals
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from common.tests import get_cover_image
from courses.models import Course, CourseSignup
from courses.signals import cover_image_resize_callback


class CoursesApiAccessTestCase(APITestCase):
    def setUp(self):
        super().setUp()
        self.list_url = reverse("courses:course-list")
        User = get_user_model()
        self.user = User.objects.create_user(
            username="test", email="test@example.com", password="test"
        )
        # Disable signals
        signals.post_save.disconnect(cover_image_resize_callback, sender=Course)

    def test_list_unauthenticated(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_authenticated(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_authenticated_without_permissions(self):
        self.client.force_authenticate(self.user)

        response = self.client.post(self.list_url, data={"name": "test course"})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_authenticated_with_permissions(self):
        permission = Permission.objects.get(
            codename="add_course", content_type=ContentType.objects.get_for_model(Course)
        )
        self.user.user_permissions.add(permission)
        self.client.force_authenticate(self.user)

        response = self.client.post(self.list_url, data={"name": "test course"})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_by_superuser(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.force_authenticate(self.user)

        response = self.client.post(self.list_url, data={"name": "test course"})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CoursesSignupApiAccessTestCase(APITestCase):
    def setUp(self):
        super().setUp()
        self.list_url = reverse("courses:course_signups-list")
        User = get_user_model()
        self.user = User.objects.create_user(
            username="test", email="test@example.com", password="test"
        )
        self.course = Course.objects.create(name="Test Course", cover_image=get_cover_image())
        self.data = {"user": self.user.id, "course": self.course.id}

    def test_unauthenticated_signup(self):
        response = self.client.post(self.list_url, data=self.data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_signup(self):
        self.client.force_authenticate(self.user)

        response = self.client.post(self.list_url, data=self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CourseSignup.objects.filter(user=self.user, course=self.course).exists())

    def test_signup_for_the_same_course_second_time(self):
        CourseSignup.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(self.user)

        response = self.client.post(self.list_url, data=self.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(), {"nonFieldErrors": ["The fields course, user must make a unique set."]}
        )

    def test_non_staff_access_to_different_user(self):
        User = get_user_model()
        other_user = User.objects.create_user(
            username="other", email="other@example.com", password="test"
        )
        other_user_signup = CourseSignup.objects.create(user=other_user, course=self.course)
        self.client.force_authenticate(self.user)

        response = self.client.get(self.list_url)

        self.assertNotIn(other_user_signup.id, [item["id"] for item in response.json()["results"]])

    def test_non_staff_access_to_own_signups(self):
        signup = CourseSignup.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(self.user)

        response = self.client.get(self.list_url)

        self.assertIn(signup.id, [item["id"] for item in response.json()["results"]])

    def test_staff_access_to_different_user_signups(self):
        User = get_user_model()
        other_user = User.objects.create_user(
            username="other", email="other@example.com", password="test"
        )
        other_user_signup = CourseSignup.objects.create(user=other_user, course=self.course)
        self.user.is_staff = True
        self.user.save()
        self.client.force_authenticate(self.user)

        response = self.client.get(self.list_url)

        self.assertIn(other_user_signup.id, [item["id"] for item in response.json()["results"]])

    def tearDown(self):
        self.course.cover_image.delete()
