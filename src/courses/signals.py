from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from courses.models import Course
from courses.tasks import test_task


def cover_image_resize_callback(sender: 'Course', *args, **kwargs):
    test_task.apply_async(args=[kwargs['instance'].id])
