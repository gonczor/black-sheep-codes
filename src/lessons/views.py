from typing import Type

from django.db import transaction
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet

from common.exceptions import ProcessingApiException, ProcessingException
from lessons.models import BaseLesson, Comment
from lessons.permissions import (
    CommentSoftDeletePermission,
    CommentUpdatePermission,
    LessonCreatePermission,
    LessonDeletePermission,
    LessonUpdatePermission,
)
from lessons.serializers import (
    BaseLessonSerializer,
    CommentCreateSerializer,
    CommentReadSerializer,
    CommentUpdateSerializer,
    ListLessonsSerializer,
)


class LessonViewSet(ModelViewSet):
    queryset = BaseLesson.objects.all()

    def get_queryset(self) -> QuerySet:
        if self.action == "list":
            self.queryset = self.queryset.with_completed_annotations(user=self.request.user)
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

    def get_serializer_context(self):
        return {"user": self.request.user}

    @transaction.atomic()
    def create(self, request: Request, *args, **kwargs) -> Response:
        return super().create(request, *args, **kwargs)

    @action(
        detail=True,
        methods=["PATCH", "POST"],
        url_path="mark-as-complete",
        url_name="mark_as_complete",
    )
    def mark_as_complete(self, request: Request, pk: int) -> Response:
        lesson = self.get_object()
        try:
            lesson.complete(user=self.request.user)
        except ProcessingException as e:
            raise ProcessingApiException(detail=e.detail) from e
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["PATCH", "POST"],
        url_path="revert-mark-as-complete",
        url_name="revert_mark_as_complete",
    )
    def revert_mark_as_complete(self, request: Request, pk: int) -> Response:
        lesson = self.get_object()
        lesson.revert_complete(user=self.request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(ModelViewSet):
    def get_permissions(self):
        permission_classes = self.permission_classes
        # Default (IsAuthenticatedPermission) for create and read.
        if self.action in {"update", "partial_update"}:
            permission_classes = [IsAuthenticated, CommentUpdatePermission]
        elif self.action == "destroy":
            permission_classes = [IsAuthenticated, CommentSoftDeletePermission]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == "create":
            return CommentCreateSerializer
        elif self.action in {"update", "partial_update"}:
            return CommentUpdateSerializer
        else:
            return CommentReadSerializer

    def get_queryset(self) -> QuerySet:
        return Comment.objects.all().prefetch_related("author")

    def get_serializer_context(self):
        return {"user": self.request.user}

    @transaction.atomic()
    def perform_create(self, serializer):
        serializer.save()

    @transaction.atomic()
    def perform_destroy(self, comment: Comment):
        comment.soft_delete()
