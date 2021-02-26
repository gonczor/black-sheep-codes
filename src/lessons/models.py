from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    FileField,
    ForeignKey,
    Model,
    TextField, QuerySet, Case, When, Value, OuterRef, Exists,
)
from polymorphic.models import PolymorphicModel

from courses.models import CourseSection
from settings import settings


def get_lesson_video_upload_directory(lesson: "Lesson", filename: str) -> str:
    return f"videos/lessons/{lesson.id}/{filename}"


def get_lesson_additional_materials_upload_directory(lesson: "Lesson", filename: str) -> str:
    return f"additional_materials/lessons/{lesson.id}/{filename}"


class BaseLessonQuerySet(QuerySet):
    def with_completed_annotations(self, user: settings.AUTH_USER_MODEL):
        completed_lesson = CompletedLesson.objects.filter(user=user, lesson=OuterRef('pk'))
        return self.annotate(
            is_completed=Case(
                When(Exists(completed_lesson), then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        )


class BaseLesson(PolymorphicModel):
    name = CharField(max_length=64)
    course_section = ForeignKey(CourseSection, on_delete=CASCADE, related_name="lessons")
    description = TextField(blank=True)

    objects = BaseLessonQuerySet.as_manager()

    class Meta:
        order_with_respect_to = "course_section"

    def is_completed_by(self, user: settings.AUTH_USER_MODEL) -> bool:
        # is_completed is annotated in with_completed_annotations queryset method.
        # However, if the queryset was not annotated, there's a fallback that performs this check.
        # Keep in mind it is far less efficient.
        if (completed := getattr(self, "is_completed", None)) is not None:
            return completed
        return CompletedLesson.objects.filter(lesson=self, user=user).exists()

    def complete(self, user: settings.AUTH_USER_MODEL):
        CompletedLesson.objects.create(lesson=self, user=user)

    def revert_complete(self, user: settings.AUTH_USER_MODEL):
        CompletedLesson.objects.filter(lesson=self, user=user).delete()


class Lesson(BaseLesson):
    video = FileField(upload_to=get_lesson_video_upload_directory, null=True, blank=True)
    additional_materials = FileField(
        upload_to=get_lesson_additional_materials_upload_directory, null=True, blank=True
    )


class Exercise(BaseLesson):
    pass


class Test(BaseLesson):
    pass


class TestQuestion(Model):
    test = ForeignKey("Test", on_delete=CASCADE, related_name="questions")
    text = TextField()


class Answer(Model):
    question = ForeignKey("TestQuestion", on_delete=CASCADE, related_name="answers")
    text = TextField()
    is_correct = BooleanField(default=False)


class CompletedLesson(Model):
    lesson = ForeignKey(BaseLesson, on_delete=CASCADE)
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    created = DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("lesson", "user")
