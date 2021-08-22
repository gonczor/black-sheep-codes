from collections import defaultdict
from typing import Dict

from drf_writable_nested import WritableNestedModelSerializer
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from rest_polymorphic.serializers import PolymorphicSerializer

from auth_ex.models import User
from lessons.models import Answer, BaseLesson, Comment, Exercise, Lesson, Test, TestQuestion


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
        fields = (
            "id",
            "name",
            "is_complete",
        )
        read_only_fields = ("is_complete",)

    is_complete = SerializerMethodField()

    def get_is_complete(self, lesson: BaseLesson) -> bool:
        return lesson.is_completed_by(user=self.context["user"])


class AnswersSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Answer
        fields = (
            "id",
            "text",
            "is_correct",
        )


class QuestionsSerializer(WritableNestedModelSerializer):
    class Meta:
        model = TestQuestion
        fields = (
            "id",
            "text",
            "answers",
        )

    answers = AnswersSerializer(
        many=True,
    )


class TestSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Test
        fields = (
            "id",
            "name",
            "course_section",
            "questions",
            "is_complete",
        )

    questions = QuestionsSerializer(many=True)
    is_complete = SerializerMethodField()

    _save_kwargs: Dict = defaultdict(dict)

    def get_is_complete(self, lesson: BaseLesson) -> bool:
        return lesson.is_completed_by(user=self.context["user"])


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


class CommentCreateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ("text", "lesson")
        read_only_fields = (
            "id",
            "author",
            "created",
        )

    def create(self, validated_data: dict) -> Comment:
        validated_data["author"] = self.context["user"]
        return super().create(validated_data)


class CommentUpdateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ("text",)


class CommentReadSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "author",
            "text",
        )
        read_only_fields = (
            "id",
            "author",
            "text",
        )
