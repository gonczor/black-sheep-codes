from django.db.models import CharField, DateTimeField, ImageField, Model, TextField
from django.db.models.signals import post_save

import courses.signals


def get_course_upload_directory(course: "Course", filename: str) -> str:
    return f"images/courses/{course.id}/{filename}"


class Course(Model):
    name = CharField(max_length=64)
    description = TextField()
    cover_image = ImageField(upload_to=get_course_upload_directory)
    small_cover_image = ImageField(null=True, blank=True, upload_to=get_course_upload_directory)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)


post_save.connect(courses.signals.cover_image_resize_callback, sender=Course)
