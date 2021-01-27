import io

from PIL import Image

from celery import shared_task

@shared_task
def test_task(course_id: int):
    from django.db.models import signals
    from courses.models import Course
    from courses.signals import cover_image_resize_callback

    # Do not call signal again
    signals.post_save.disconnect(cover_image_resize_callback, sender=Course)

    course = Course.objects.get(id=course_id)

    with Image.open(course.cover_image) as original_image:
        original_height = original_image.height
        original_width = original_image.width
        new_width = 200
        new_height = int((new_width / original_width) * original_height)
        new_image = original_image.resize((new_width, new_height))

        output = io.BytesIO()
        new_image.save(output, format='JPEG')
        output.seek(0)

        name_parts = course.cover_image.name.split('.')
        name = ''.join(name_parts[:-1]) + '_small' + '.' + name_parts[-1]
        course.small_cover_image.save(name, output, save=False)
        course.save()

    signals.post_save.connect(cover_image_resize_callback, sender=Course)
    return course_id
