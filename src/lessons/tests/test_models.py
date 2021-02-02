from unittest import TestCase

from courses.models import Course, CourseSection
from lessons.models import Lesson, Exercise, Test


class LessonModelsTestCase(TestCase):
    # Those tests are mainly to prove correct usage of certain mechanisms and prevent from
    # regressions should the used libraries become obsolete.
    def setUp(self):
        self.course = Course.objects.create(name="test")
        self.course_section = CourseSection.objects.create(course=self.course, name="test section")
        self.lesson = Lesson.objects.create(course_section=self.course_section)
        self.exercise = Exercise.objects.create(course_section=self.course_section)
        self.test = Test.objects.create(course_section=self.course_section)

    def test_access_to_polymorphic_relations(self):
        self.assertEqual(self.course_section.lessons.count(), 3)
        self.assertEqual(self.course_section.lessons.instance_of(Lesson).get(), self.lesson)
        self.assertEqual(self.course_section.lessons.instance_of(Exercise).get(), self.exercise)
        self.assertEqual(self.course_section.lessons.instance_of(Test).get(), self.test)

    def test_ordering_of_polymorphic_relations(self):
        lessons_order = list(
            self.course_section.get_baselesson_order().values_list("id", flat=True)
        )

        self.assertEqual(
            lessons_order,
            [self.lesson.id, self.exercise.id, self.test.id]
        )

        self.course_section.set_baselesson_order(lessons_order[::-1])
        lessons_order = list(
            self.course_section.get_baselesson_order().values_list("id", flat=True)
        )

        self.assertEqual(
            lessons_order,
            [self.test.id, self.exercise.id, self.lesson.id]
        )
