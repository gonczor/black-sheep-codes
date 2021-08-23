from unittest.mock import patch

from django.test import TestCase

from courses.models import Course


class CourseTestCase(TestCase):
    def test_delete_cover_image_is_called(self):
        course = Course.objects.create(name="test")
        with patch("courses.signals._delete_cover_image") as mock_delete:
            course.delete()
            mock_delete.assert_called()
