from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, response
from django.conf import settings

from users.models import MyUser
from auch.serializers import SignupSerializer, TokenSerializer


@api_view(['POST'])
@permission_classes([AllowAny,])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if not serializer.is_valid():
        return response.Response(serializer.errors,
                                 status=status.HTTP_400_BAD_REQUEST)
    email = serializer.validated_data['email']
    username = serializer.validated_data['username']
    if username == 'me':
        return response.Response(serializer.errors,
                                 status=status.HTTP_400_BAD_REQUEST)
    user, _ = MyUser.objects.get_or_create(username=username,
                                           defaults={'email': email},)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Аунтефикация пользователей YAMDB',
        message=f'Код для аунтефикации: {confirmation_code}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email,],
        fail_silently=False,
    )
    return response.Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny,])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    if not serializer.is_valid():
        return response.Response(serializer.errors,
                                 status=status.HTTP_400_BAD_REQUEST)
    username = serializer.validated_data['username']
    confirmation_code = serializer.validated_data['confirmation_code']
    user = get_object_or_404(MyUser, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        refresh = RefreshToken.for_user(user)
        return JsonResponse({'token': str(refresh.access_token)},
                            status=status.HTTP_200_OK)
    return response.Response(serializer.errors,
                             status=status.HTTP_400_BAD_REQUEST)
