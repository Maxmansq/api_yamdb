from rest_framework import permissions

from users.models import MyUser


class IsAdminOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.effective_role == MyUser.Role.ADMIN)

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated
                and request.user.effective_role == MyUser.Role.ADMIN)


class MyUserOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj == request.user
