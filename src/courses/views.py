from typing import Type

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet

from courses.models import Course
from courses.permissions import CoursesManagementPermission
from courses.serializers import CourseDetailSerializer, CourseSerializer


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

    @action(detail=True)
    def signup(self, request: Request, pk: int) -> Response:
        data = None
        return Response()
