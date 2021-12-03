import io
from typing import TYPE_CHECKING

from celery import shared_task
from PIL import Image

if TYPE_CHECKING:
    from courses.models import Course


@shared_task
def resize_course_cover_image(course_id: int):
    from django.db.models import signals

    from courses.models import Course
    from courses.signals import cover_image_resize_callback

    course = Course.objects.get(id=course_id)
    if _does_not_have_image(course):
        return
    if not _image_changed(course):
        return
    try:
        # Do not call signal again
        signals.post_save.disconnect(cover_image_resize_callback, sender=Course)

        with Image.open(course.cover_image) as original_image:
            new_width, new_height = _get_small_size(original_image)
            new_image = original_image.resize((new_width, new_height))
            _save_resized(new_image, course)

    except Exception:
        raise
    finally:
        signals.post_save.connect(cover_image_resize_callback, sender=Course)


def _get_small_size(original_image: Image) -> tuple[int, int]:
    original_height = original_image.height
    original_width = original_image.width
    new_width = 200
    new_height = int((new_width / original_width) * original_height)

    return new_width, new_height


def _save_resized(new_image: Image, course: "Course"):
    output = io.BytesIO()
    new_image.save(output, format="JPEG")
    output.seek(0)
    name_parts = course.cover_image.name.split("/")[-1].split(".")
    name = "".join(name_parts[:-1]) + "_small" + "." + name_parts[-1]
    course.small_cover_image.save(name, output, save=False)
    course.save()


def _does_not_have_image(course: "Course") -> bool:
    return course.cover_image.name == ""


def _image_changed(course: "Course") -> bool:
    """
    The small cover image has the same name appended by _small suffix.
    If the name of the small image name does not start with the full
    image name, it means that a change has taken place.
    """
    if course.small_cover_image.name == "":
        return True
    full_image_base_name = course.cover_image.name.split("/")[-1].split(".")[0]
    small_image_base_name = course.small_cover_image.name.split("/")[-1].split(".")[0]
    return not small_image_base_name.startswith(full_image_base_name)
