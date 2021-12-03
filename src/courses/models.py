from uuid import uuid4

from django.conf import settings
from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    ForeignKey,
    ImageField,
    Model,
    TextField,
    UUIDField,
)
from django.db.models.signals import post_delete, post_save, pre_save

from courses.querysets import CourseQuerySet
from courses.signals import (
    cover_image_resize_callback,
    delete_cover_images,
    delete_images_if_changed,
)


def get_course_upload_directory(course: "Course", filename: str) -> str:
    return f"images/courses/{course.file_uuid}/{filename}"


class Course(Model):
    name = CharField(max_length=64)
    description = TextField()
    cover_image = ImageField(upload_to=get_course_upload_directory)
    small_cover_image = ImageField(null=True, blank=True, upload_to=get_course_upload_directory)
    file_uuid = UUIDField(
        default=uuid4,
        unique=True,
        editable=False,
    )
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    objects = CourseQuerySet.as_manager()

    def __str__(self):
        return f"{self.name} ({self.id})"


class CourseSection(Model):
    course = ForeignKey(Course, on_delete=CASCADE, related_name="course_sections")
    name = CharField(max_length=64)

    class Meta:
        order_with_respect_to = "course"

    def __str__(self):
        return f"{self.name} ({self.id}) - {self.course}"


class CourseSignup(Model):
    course = ForeignKey(Course, related_name="signups", on_delete=CASCADE)
    user = ForeignKey(settings.AUTH_USER_MODEL, related_name="signups", on_delete=CASCADE)

    class Meta:
        unique_together = ("course", "user")


post_save.connect(cover_image_resize_callback, sender=Course)
post_delete.connect(delete_cover_images, sender=Course)
pre_save.connect(delete_images_if_changed, sender=Course)
