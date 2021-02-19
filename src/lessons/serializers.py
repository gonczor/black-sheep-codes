from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from rest_polymorphic.serializers import PolymorphicSerializer

from lessons.models import BaseLesson, Exercise, Lesson, Test


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = (
            "id",
            "name",
            "description",
            "video",
            "additional_materials",
            "course_section",
            "is_complete",
        )
        read_only_fields = ("is_complete",)

    is_complete = SerializerMethodField()

    def get_is_complete(self, lesson: BaseLesson) -> bool:
        return lesson.is_completed_by(user=self.context["user"])


class ExerciseSerializer(ModelSerializer):
    class Meta:
        model = Exercise
        fields = "__all__"


class TestSerializer(ModelSerializer):
    class Meta:
        model = Test
        fields = "__all__"


class BaseLessonSerializer(PolymorphicSerializer):
    resource_type_field_name = "lesson_type"

    model_serializer_mapping = {
        Lesson: LessonSerializer,
        Exercise: ExerciseSerializer,
        Test: TestSerializer,
    }


class ListLessonsSerializer(ModelSerializer):
    class Meta:
        model = BaseLesson
        fields = (
            "id",
            "name",
            "is_complete",
        )
        read_only_fields = ("is_complete",)

    is_complete = SerializerMethodField()

    def get_is_complete(self, lesson: BaseLesson) -> bool:
        return lesson.is_completed_by(user=self.context["user"])
