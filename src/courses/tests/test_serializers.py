from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import signals
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from courses.models import Course, CourseSignup, CourseSection
from courses.serializers import CourseSectionReorderSerializer
from courses.signals import cover_image_resize_callback


class CourseSectionReorderSerializerTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.course = Course.objects.create(name="Test Course")
        # Disable signals
        signals.post_save.disconnect(cover_image_resize_callback, sender=Course)

    def tearDown(self):
        self.course.cover_image.delete(save=True)
        signals.post_save.connect(cover_image_resize_callback, sender=Course)

    def test_non_existent_section(self):
        serializer = CourseSectionReorderSerializer(instance=self.course, data={"sections": [1]})

        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors,
            {'sections': [ErrorDetail(string='Invalid pk "1" - object does not exist.', code='does_not_exist')]}
        )

    def test_reorder_section(self):
        section1 = CourseSection.objects.create(course=self.course)
        section2 = CourseSection.objects.create(course=self.course)
        data = {"sections": [section2.id, section1.id]}
        serializer = CourseSectionReorderSerializer(instance=self.course, data=data)

        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertEqual(
            list(self.course.get_coursesection_order().values_list("id", flat=True)),
            [section2.id, section1.id]
        )
