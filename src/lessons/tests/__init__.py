from unittest import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

from courses.models import Course, CourseSection
from lessons.models import Exercise, Lesson, Test, Comment


class BaseLessonTestCase(TestCase):
    def setUp(self):
        self.course = Course.objects.create(name="test")
        self.course_section = CourseSection.objects.create(course=self.course, name="test section")
        self.lesson = Lesson.objects.create(course_section=self.course_section)
        self.exercise = Exercise.objects.create(course_section=self.course_section)
        self.test = Test.objects.create(course_section=self.course_section)


class BaseCommentTestCase(BaseLessonTestCase):
    def setUp(self):
        super().setUp()
        User = get_user_model()
        self.author = User.objects.create_user(
            username="test", email="test@example.com", password="test"
        )
        self.comment = Comment.objects.create(
            author=self.author, text="Some comment", lesson=self.lesson
        )
        self.list_url = reverse("lessons:comment-list")
        self.detail_url = reverse("lessons:comment-detail", args=(self.comment.pk,))
