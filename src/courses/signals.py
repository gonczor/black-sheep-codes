from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from courses.models import Course
from courses.tasks import resize_course_cover_image


def cover_image_resize_callback(sender: "Course", *args, **kwargs):
    resize_course_cover_image.apply_async(args=[kwargs["instance"].id])


# Extracted code to make testing easier.
def _delete_cover_image(instance: "Course"):
    instance.cover_image.delete(save=False)
    instance.small_cover_image.delete(save=False)


def delete_cover_images(sender: "Course", instance, *args, **kwargs):
    _delete_cover_image(instance)
