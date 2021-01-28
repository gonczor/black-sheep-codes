from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet


class CoursesManagementPermission(BasePermission):
    def has_permission(self, request: Request, view: ViewSet) -> bool:
        return request.user.has_perm("courses.add_course")
