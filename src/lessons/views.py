from typing import Type

from django.db import IntegrityError
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
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

    def get_queryset(self) -> QuerySet:
        if not self.request.user.is_staff and not self.request.user.is_superuser:
            return self.queryset.filter(course_section__course__signups__user=self.request.user)
        return self.queryset

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

    @action(
        detail=True, methods=["PATCH"], url_path="mark-as-complete", url_name="mark_as_complete"
    )
    def mark_as_complete(self, request: Request, pk: int) -> Response:
        lesson = self.get_object()
        try:
            lesson.complete(user=self.request.user)
        except IntegrityError:
            return Response(
                status=status.HTTP_409_CONFLICT,
                data={"non_field_errors": ["Already marked as complete."]},
            )
        return Response(status=status.HTTP_204_NO_CONTENT)
