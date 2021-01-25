from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import signals
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Course
from courses.signals import cover_image_resize_callback


class CoursesApiAccessTestCase(APITestCase):
    def setUp(self):
        super().setUp()
        self.list_url = reverse('courses:course-list')
        User = get_user_model()
        self.user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='test'
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

        response = self.client.post(self.list_url, data={'name': 'test course'})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_authenticated_with_permissions(self):
        permission = Permission.objects.get(
            codename='add_course', content_type=ContentType.objects.get_for_model(Course)
        )
        self.user.user_permissions.add(permission)
        self.client.force_authenticate(self.user)

        response = self.client.post(self.list_url, data={'name': 'test course'})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_by_superuser(self):
        self.user.is_superuser = True
        self.user.save()
        self.client.force_authenticate(self.user)

        response = self.client.post(self.list_url, data={'name': 'test course'})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
