from typing import Type

from django.db.models import QuerySet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet

from courses.models import Course, CourseSignup
from courses.permissions import CoursesManagementPermission
from courses.serializers import CourseDetailSerializer, CourseSerializer, SignupSerializer


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "retrieve":
            return CourseDetailSerializer
        else:
            return CourseSerializer

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action in {"create", "update", "partial_update", "delete"}:
            permission_classes = [IsAuthenticated, CoursesManagementPermission]
        return [permission() for permission in permission_classes]


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
