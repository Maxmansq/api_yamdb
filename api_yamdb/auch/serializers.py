from rest_framework import serializers

from users.models import CastomUser
from users.serializers import CreateValidateSerializers


class SignupSerializer(CreateValidateSerializers):
    """Сериализатор для регистрации пользователя"""

    class Meta:
        model = CastomUser
        fields = ["email", "username"]


class TokenSerializer(serializers.Serializer):
    """Сериализватор для получения JWT токена"""
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=150)

    class Meta:
        model = CastomUser
