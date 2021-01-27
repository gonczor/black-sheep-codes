from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from courses.models import Course
from courses.tasks import resize_course_cover_image


def cover_image_resize_callback(sender: 'Course', *args, **kwargs):
    resize_course_cover_image.apply_async(args=[kwargs['instance'].id])
