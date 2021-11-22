import io
from typing import TYPE_CHECKING

from PIL import Image

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


def delete_images_if_changed(sender: "Course", instance, *args, **kwargs):
    from .models import Course

    if instance.pk is None:
        return
    old_course = Course.objects.get(pk=instance.pk)
    if instance.cover_image.name != old_course.cover_image.name:
        _delete_cover_image(old_course)
