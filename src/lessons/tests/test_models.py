from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from parameterized import parameterized

from common.exceptions import ProcessingException
from lessons.models import BaseLesson, Comment, Exercise, Lesson, Test
from lessons.tests import BaseLessonTestCase


class LessonModelsTestCase(BaseLessonTestCase, TestCase):
    # Those tests are mainly to prove correct usage of certain mechanisms and prevent from
    # regressions should the used libraries become obsolete.

    def test_access_to_polymorphic_relations(self):
        self.assertEqual(self.course_section.lessons.count(), 3)
        self.assertEqual(self.course_section.lessons.instance_of(Lesson).get(), self.lesson)
        self.assertEqual(self.course_section.lessons.instance_of(Exercise).get(), self.exercise)
        self.assertEqual(self.course_section.lessons.instance_of(Test).get(), self.test)

    def test_ordering_of_polymorphic_relations(self):
        lessons_order = list(
            self.course_section.get_baselesson_order().values_list("id", flat=True)
        )

        self.assertEqual(lessons_order, [self.lesson.id, self.exercise.id, self.test.id])

        self.course_section.set_baselesson_order(lessons_order[::-1])
        lessons_order = list(
            self.course_section.get_baselesson_order().values_list("id", flat=True)
        )

        self.assertEqual(lessons_order, [self.test.id, self.exercise.id, self.lesson.id])

    @parameterized.expand([("lesson", "lesson"), ("exercise", "exercise"), ("test", "test")])
    def test_is_completed_by(self, _: str, lesson_type: str):
        User = get_user_model()
        user = User.objects.create_user(username="test", email="test@example.com", password="test")

        lesson = getattr(self, lesson_type)

        self.assertFalse(lesson.is_completed_by(user))
        lesson.complete(user)
        self.assertTrue(lesson.is_completed_by(user))

    @parameterized.expand([("lesson", "lesson"), ("exercise", "exercise"), ("test", "test")])
    def test_revert_complete(self, _: str, lesson_type: str):
        User = get_user_model()
        user = User.objects.create_user(username="test", email="test@example.com", password="test")

        lesson = getattr(self, lesson_type)
        lesson.complete(user)

        self.assertTrue(lesson.is_completed_by(user))
        lesson.revert_complete(user)
        self.assertFalse(lesson.is_completed_by(user))

    @parameterized.expand([("lesson", "lesson"), ("exercise", "exercise"), ("test", "test")])
    def test_duplicate_complete(self, _: str, lesson_type: str):
        User = get_user_model()
        user = User.objects.create_user(
            username="tests", email="tests@example.com", password="test"
        )
        lesson = getattr(self, lesson_type)
        lesson.complete(user)

        with self.assertRaises(ProcessingException):
            lesson.complete(user)

    def test_annotate_completed(self):
        User = get_user_model()
        user = User.objects.create_user(username="test", email="test@example.com", password="test")

        for lesson in BaseLesson.objects.all().with_completed_annotations(user=user):
            self.assertFalse(lesson.is_completed)

        for lesson in BaseLesson.objects.all():
            lesson.complete(user)

        for lesson in BaseLesson.objects.all().with_completed_annotations(user=user):
            self.assertTrue(lesson.is_completed)


class CommentTestCase(BaseLessonTestCase, TestCase):
    def test_does_not_list_deleted_by_default(self):
        Comment.objects.create(lesson=self.lesson, deleted=True)
        self.assertEqual(Comment.objects.count(), 0)

    def test_lists_deleted_with_deleted_manager(self):
        Comment.objects.create(lesson=self.lesson, deleted=True)
        self.assertEqual(Comment.deleted_objects.count(), 1)
