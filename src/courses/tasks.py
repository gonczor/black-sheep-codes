import io
from typing import TYPE_CHECKING

from settings.celery import app

from celery import shared_task
from PIL import Image

if TYPE_CHECKING:
    from courses.models import Course


@shared_task
def resize_course_cover_image(course_id: int):
    from django.db.models import signals

    from courses.models import Course
    from courses.signals import cover_image_resize_callback

    try:
        # Do not call signal again
        signals.post_save.disconnect(cover_image_resize_callback, sender=Course)

        course = Course.objects.get(id=course_id)

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


def publish_message():
    with app.producer_pool.acquire(block=True) as producer:
        producer.publish(
            body={"TEST": "OK"},
            exchange='myexchange',
            routing_key='mykey',
        )


@shared_task()
def consume_message_1(*args, **kwargs):
    print(f"## 1 ##\nARGS: {args}\nKWARGS: {kwargs}")


@shared_task
def consume_message_2(*args, **kwargs):
    print(f"## 2 @@\nARGS: {args}\nKWARGS: {kwargs}")
