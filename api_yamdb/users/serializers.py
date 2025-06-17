from rest_framework import serializers

from users.models import MyUser


class CreateValidateSerializers(serializers.ModelSerializer):
    """Сериализватор для регистрации пользователей"""
    email = serializers.EmailField(max_length=254,)
    username = serializers.RegexField(
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

        if username == 'me':
            raise serializers.ValidationError({
                "username": "Это имя недопустимо."
            })
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

    def update(self, instance, validated_data):
        request = self.context.get('request', None)
        user = request.user
        if user.role != MyUser.Role.ADMIN:
            validated_data.pop('role', None)
        return super().update(instance, validated_data)


class UsersSerializers(CreateValidateSerializers):
    """Сериализатор для GET запроса пользователей"""
    class Meta:
        fields = ['username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role']
        model = MyUser
