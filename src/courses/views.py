from typing import Type

from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet

from courses.models import Course
from courses.permissions import CoursesPermission
from courses.serializers import CourseDetailSerializer, CourseSerializer


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated, CoursesPermission]

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == 'retrieve':
            return CourseDetailSerializer
        else:
            return CourseSerializer
