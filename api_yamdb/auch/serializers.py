from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import MyUser


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    username = username = serializers.RegexField(
        max_length=150,
        regex=r'^[\w.@+-]+\Z',
        required=True,
        error_messages={
            "invalid": "Имя пользователя содержит недопустимые символы.",
            "blank": "Обязательное поле.",
        })
    def validate(self, attrs):
        email = attrs.get("email")
        username = attrs.get("username")
        reg_user = MyUser.objects.filter(username=username).first()
        reg_email = MyUser.objects.filter(email=email).first()

        if reg_user and reg_user.email == email:
            return attrs
        if reg_user:
            raise serializers.ValidationError({
                "username": "Это имя пользователя уже занято."
            })
        if reg_email:
            raise serializers.ValidationError({
                "email": "Пользователь с таким email уже существует."
            })
        return attrs

    def create(self, validated_data):
        return MyUser.objects.create(**validated_data)



    class Meta:
        model = MyUser


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=150)

    class Meta:
        model = MyUser
