from rest_framework import permissions

from users.models import MyUser


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user.is_authenticated 
                and request.user.effective_role == MyUser.Role.ADMIN)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user.is_authenticated
                and request.user.effective_role == MyUser.Role.ADMIN)
