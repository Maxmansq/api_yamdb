from rest_framework import viewsets, response, permissions, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import action

from users.models import CastomUser
from users.serializers import UsersSerializers
from users.permissions import IsAdminOnly, ISMyUserOnly


class UsersViewSet(viewsets.ModelViewSet):
    """Пользователь"""
    queryset = CastomUser.objects.all()
    serializer_class = UsersSerializers
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    lookup_field = "username"
    http_method_names = ["get", "patch", "post", "delete"]

    @action(detail=False,
            methods=["get", "patch"],
            url_path="me",
            permission_classes=[permissions.IsAuthenticated, ISMyUserOnly])
    def get_personal_user(self, request):
        user = CastomUser.objects.get(username=request.user.username)
        if request.method == "PATCH":
            serializer = UsersSerializers(user,
                                          data=request.data,
                                          partial=True,
                                          context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return response.Response({
                "message": "Получены данные",
                "data": serializer.data
            })
        serializer = UsersSerializers(user)
        return response.Response(serializer.data)
