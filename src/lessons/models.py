from django.db.models import CASCADE, CharField, FileField, ForeignKey, TextField, Model, \
    DateTimeField
from polymorphic.models import PolymorphicModel

from courses.models import CourseSection
from settings import settings


def get_lesson_video_upload_directory(lesson: "Lesson", filename: str) -> str:
    return f"videos/lessons/{lesson.id}/{filename}"


def get_lesson_additional_materials_upload_directory(lesson: "Lesson", filename: str) -> str:
    return f"additional_materials/lessons/{lesson.id}/{filename}"


class BaseLesson(PolymorphicModel):
    name = CharField(max_length=64)
    course_section = ForeignKey(CourseSection, on_delete=CASCADE, related_name="lessons")
    description = TextField(blank=True)

    class Meta:
        order_with_respect_to = "course_section"

    def is_completed_by(self, user: settings.AUTH_USER_MODEL) -> bool:
        return CompletedLesson.objects.filter(lesson=self, user=user).exists()

    def complete(self, user: settings.AUTH_USER_MODEL):
        CompletedLesson.objects.create(lesson=self, user=user)


class Lesson(BaseLesson):
    video = FileField(upload_to=get_lesson_video_upload_directory, null=True, blank=True)
    additional_materials = FileField(
        upload_to=get_lesson_additional_materials_upload_directory, null=True, blank=True
    )


class Exercise(BaseLesson):
    pass


class Test(BaseLesson):
    pass


class CompletedLesson(Model):
    lesson = ForeignKey(BaseLesson, on_delete=CASCADE)
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    created = DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("lesson", "user")
