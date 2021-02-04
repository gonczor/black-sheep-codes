from unittest import TestCase
from courses.models import Course, CourseSection
from lessons.models import Lesson, Exercise, Test


class BaseLessonTestCase(TestCase):
    def setUp(self):
        self.course = Course.objects.create(name="test")
        self.course_section = CourseSection.objects.create(course=self.course, name="test section")
        self.lesson = Lesson.objects.create(course_section=self.course_section)
        self.exercise = Exercise.objects.create(course_section=self.course_section)
        self.test = Test.objects.create(course_section=self.course_section)
