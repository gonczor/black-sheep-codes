from typing import Type

from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet

from lessons.models import BaseLesson
from lessons.serializers import ListLessonsSerializer, BaseLessonSerializer


class LessonViewSet(ModelViewSet):
    queryset = BaseLesson.objects.all()

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "list":
            return ListLessonsSerializer
        else:
            return BaseLessonSerializer
