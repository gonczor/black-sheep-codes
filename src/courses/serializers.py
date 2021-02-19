from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.validators import UniqueTogetherValidator

from courses.models import Course, CourseSection, CourseSignup
from lessons.serializers import ListLessonsSerializer


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "name")


class CourseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "name", "image", "description")

    image = serializers.SerializerMethodField()

    def get_image(self, course: Course) -> str:
        if course.small_cover_image:
            return course.small_cover_image.url
        else:
            return course.cover_image.url


class CourseSectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSection
        fields = ("id", "name", "lessons")

    lessons = ListLessonsSerializer(many=True)


class CourseWithLessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "name", "sections")

    sections = CourseSectionsSerializer(many=True, source="course_sections")


class CourseSectionReorderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("sections",)

    sections = PrimaryKeyRelatedField(many=True, queryset=CourseSection.objects.all())

    def update(self, course: Course, validated_data: dict) -> Course:
        course.set_coursesection_order((section.id for section in validated_data["sections"]))
        return course


class SignupSerializer(serializers.ModelSerializer):
    validators = [
        UniqueTogetherValidator(
            queryset=CourseSignup.objects.all(),
            fields=["user", "course"],
            message="Already signed up for this course.",
        )
    ]

    class Meta:
        model = CourseSignup
        fields = (
            "id",
            "user",
            "course",
        )
