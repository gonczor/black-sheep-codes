from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from courses.models import CourseSignup
from lessons.models import Answer, Test, TestQuestion, Lesson
from lessons.tests import BaseLessonTestCase


class LessonAPITestCase(APITestCase, BaseLessonTestCase):
    def setUp(self):
        super().setUp()
        self.mark_as_complete_url = reverse(
            "lessons:lesson-mark_as_complete", args=(self.lesson.id,)
        )
        self.revert_mark_as_complete_url = reverse(
            "lessons:lesson-revert_mark_as_complete", args=(self.lesson.id,)
        )
        self.lesson_create_url = reverse("lessons:lesson-list")
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

    def test_nested_test_lesson_serializer(self):
        self.user.is_superuser = True
        self.user.save()
        create_data = {
            "course_section": self.course_section.id,
            "name": "Some Test",
            "lesson_type": "Test",
            "questions": [
                {
                    "text": 'How to print "Hello, world!"?',
                    "answers": [
                        {"text": 'System.out.println("Hello, world!");', "is_correct": False},
                        {"text": 'print("Hello, world!")', "is_correct": True},
                    ],
                },
            ],
        }
        self.client.force_authenticate(self.user)

        import json

        create_data = json.dumps(create_data)
        response = self.client.post(
            self.lesson_create_url, data=create_data, content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Test.objects.filter(course_section=self.course_section).exists())
        self.assertTrue(
            TestQuestion.objects.filter(test__course_section=self.course_section).exists()
        )
        self.assertEqual(
            Answer.objects.filter(question__test__course_section=self.course_section).count(), 2
        )

    def test_number_of_queries_on_list(self):
        self.client.force_authenticate(self.user)

        # Without prefetch there were 8.
        with self.assertNumQueries(5):
            self.client.get(self.lesson_create_url)
