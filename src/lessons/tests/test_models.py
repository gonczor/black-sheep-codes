from django.contrib.auth import get_user_model
from django.db import IntegrityError

from lessons.models import Exercise, Lesson, Test
from lessons.tests import BaseLessonTestCase


class LessonModelsTestCase(BaseLessonTestCase):
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

    def test_is_completed_by(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="test", email="test@example.com", password="test"
        )

        self.assertFalse(self.lesson.is_completed_by(user))
        self.lesson.complete(user)
        self.assertTrue(self.lesson.is_completed_by(user))

    def test_duplicate_complete(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="tests", email="tests@example.com", password="test"
        )
        self.lesson.complete(user)

        with self.assertRaises(IntegrityError):
            self.lesson.complete(user)
