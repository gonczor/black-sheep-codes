from unittest.mock import patch

from django.test import TestCase

from common.tests import get_cover_image
from courses.models import Course


class CourseTestCase(TestCase):
    def test_delete_cover_image_is_called(self):
        course = Course.objects.create(name="test")
        with patch("courses.signals._delete_cover_image") as mock_delete:
            course.delete()
            mock_delete.assert_called()

    def test_old_cover_is_deleted_on_change(self):
        with patch("courses.signals._delete_cover_image") as mock_delete:
            c = Course.objects.create(name="test", cover_image=get_cover_image())
            c.cover_image = get_cover_image("new_name.jpg")
            c.save()
            mock_delete.assert_called()

    def test_image_is_not_resized_when_image_is_not_changed(self):
        c = Course.objects.create(
            name="test", cover_image=get_cover_image(), small_cover_image=get_cover_image()
        )
        with patch("courses.tasks._save_resized") as mock_delete:
            c.name = "New test"
            c.save()
            mock_delete.assert_not_called()
