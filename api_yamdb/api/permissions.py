from rest_framework import permissions

from users.models import CastomUser


class IsAdminOrReadOnly(permissions.BasePermission):
    """Доступ на изменения только админам"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user.is_authenticated
                and request.user.effective_role == CastomUser.Role.ADMIN)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user.is_authenticated
                and request.user.effective_role == CastomUser.Role.ADMIN)


class IsAuthorOrModeratorOrAdminOrReadOnly(permissions.BasePermission):
    """Доступ на именения только модераторам и админам"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (
            obj.author == request.user
            or request.user.effective_role == CastomUser.Role.ADMIN
            or request.user.effective_role == CastomUser.Role.MODERATOR
        )
