from rest_framework.serializers import ModelSerializer
from rest_polymorphic.serializers import PolymorphicSerializer

from lessons.models import BaseLesson, Exercise, Lesson, Test


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


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
        fields = ("id", "name")
