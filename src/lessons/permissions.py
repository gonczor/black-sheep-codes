from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet


class LessonCreatePermission(BasePermission):
    def has_permission(self, request: Request, view: ViewSet) -> bool:
        return request.user.has_perm("lessons.add_baselesson")


class LessonUpdatePermission(BasePermission):
    def has_permission(self, request: Request, view: ViewSet) -> bool:
        return request.user.has_perm("lessons.change_baselesson")


class LessonDeletePermission(BasePermission):
    def has_permission(self, request: Request, view: ViewSet) -> bool:
        return request.user.has_perm("lessons.delete_baselesson")


class CommentSoftDeletePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("lessons.soft_delete_comment")


class CommentUpdatePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("lessons.change_comment")


class CommentDeletePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("lessons.delete_comment")
