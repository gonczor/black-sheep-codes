from rest_framework import serializers

from courses.models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'name')


class CourseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('name', 'cover_image', 'description')
