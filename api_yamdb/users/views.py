from rest_framework import viewsets, response, permissions, status, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import action

from users.models import MyUser
from users.serializers import UsersSerializers
from users.permissions import IsAdminOnly, MyUserOnly


class UsersViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UsersSerializers
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'patch', 'post', 'delete']

    @action(detail=False,
            methods=['get', 'patch'],
            url_path='me',
            permission_classes=[permissions.IsAuthenticated, MyUserOnly])
    def PersonalUser(self, request):
        user = MyUser.objects.get(username=request.user.username)
        if request.method == 'PATCH':
            serializer = UsersSerializers(user,
                                          data=request.data,
                                          partial=True,
                                          context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return response.Response({'message': 'Получены данные',
                                          'data': request.data})
            else:
                return response.Response(serializer.errors,
                                         status=status.HTTP_400_BAD_REQUEST)
        serializer = UsersSerializers(user)
        return response.Response(serializer.data)
