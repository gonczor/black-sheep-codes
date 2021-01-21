from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet


class CoursesPermission(BasePermission):
    def has_permission(self, request: Request, view: ViewSet) -> bool:
        if view.action == 'create':
            return request.user.has_perm('courses.add_course')
        return True
