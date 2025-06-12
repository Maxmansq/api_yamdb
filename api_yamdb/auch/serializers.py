from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import MyUser
from users.serializers import CreateValidateSerializers


class SignupSerializer(CreateValidateSerializers):

    class Meta:
        model = MyUser
        fields = ['email', 'username',]


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=150)

    class Meta:
        model = MyUser
