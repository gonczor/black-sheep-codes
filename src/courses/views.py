from typing import Type

from django.db.models import QuerySet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet

from courses.models import Course, CourseSignup
from courses.permissions import (
    CourseDeletePermission,
    CourseEditPermission,
    CoursesCreatePermission,
)
from courses.serializers import (
    CourseDetailSerializer,
    CourseSectionReorderSerializer,
    CourseSerializer,
    SignupSerializer,
)


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        queryset = self.queryset
        if self.action == "list_assigned":
            queryset = queryset.filter(signups__user=self.request.user)
        return queryset

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "retrieve":
            return CourseDetailSerializer
        elif self.action == "reorder_sections":
            return CourseSectionReorderSerializer
        else:
            return CourseSerializer

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action == "create":
            permission_classes = [IsAuthenticated, CoursesCreatePermission]
        elif self.action in {"retrieve", "list"}:
            permission_classes = self.permission_classes
        elif self.action in {"create", "update", "partial_update", "reorder_sections"}:
            permission_classes = [IsAuthenticated, CourseEditPermission]
        elif self.action == "delete":
            permission_classes = [IsAuthenticated, CourseDeletePermission]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=["PATCH"], url_path="reorder-sections")
    def reorder_sections(self, request: Request, pk: int) -> Response:
        course = self.get_object()
        serializer = self.get_serializer(instance=course, data=self.request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["GET"], url_path="list-assigned")
    def list_assigned(self, request: Request) -> Response:
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(instance=queryset, many=True)
        return self.get_paginated_response(serializer.data)


class CourseSignupView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SignupSerializer

    def get_queryset(self) -> QuerySet:
        if self.request.user.is_staff:
            return CourseSignup.objects.all()
        else:
            return CourseSignup.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data
        data["user"] = self.request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
