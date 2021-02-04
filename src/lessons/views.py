from typing import Type

from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet

from lessons.models import BaseLesson
from lessons.permissions import (
    LessonCreatePermission,
    LessonDeletePermission,
    LessonUpdatePermission,
)
from lessons.serializers import BaseLessonSerializer, ListLessonsSerializer


class LessonViewSet(ModelViewSet):
    queryset = BaseLesson.objects.all()

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action == "create":
            permission_classes = [IsAuthenticated, LessonCreatePermission]
        elif self.action in {"update", "partial_update"}:
            permission_classes = [IsAuthenticated, LessonUpdatePermission]
        elif self.action == "destroy":
            permission_classes = [IsAuthenticated, LessonDeletePermission]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "list":
            return ListLessonsSerializer
        else:
            return BaseLessonSerializer
