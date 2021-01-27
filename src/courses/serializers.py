from rest_framework import serializers

from courses.models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'name')


class CourseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('name', 'image', 'description')

    image = serializers.SerializerMethodField()

    def get_image(self, course: Course) -> str:
        if course.small_cover_image:
            return course.small_cover_image.url
        else:
            return course.cover_image.url
