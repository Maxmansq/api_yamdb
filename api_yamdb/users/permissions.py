from rest_framework import permissions

from users.models import CastomUser


class IsAdminOnly(permissions.BasePermission):
    """Доступ только админу"""
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.effective_role == CastomUser.Role.ADMIN)

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated
                and request.user.effective_role == CastomUser.Role.ADMIN)


class ISMyUserOnly(permissions.BasePermission):
    """Доступ только автору"""
    def has_object_permission(self, request, view, obj):
        return obj == request.user
