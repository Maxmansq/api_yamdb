from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий"""
    class Meta:
        model = Category
        fields = ("name", "slug")
        lookup_field = "slug"


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров"""
    class Meta:
        model = Genre
        fields = ("name", "slug")
        lookup_field = "slug"


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения произведений"""
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = "__all__"


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для изменения или добавления произведения"""
    genre = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = "__all__"

class ReviewSerializer(serializers.ModelSerializer):
    class CurrentTitleDefault:
        requires_context = True

        def __call__(self, serializer_field):
            return serializer_field.context['title']

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    title = serializers.PrimaryKeyRelatedField(
        queryset=Title.objects.all(),
        default=CurrentTitleDefault(),
        write_only=True
    )

    title = serializers.PrimaryKeyRelatedField(
        queryset=Title.objects.all(),
        default=CurrentTitleDefault(),
        write_only=True
    )

    class Meta:
        model = Review
        fields = ['id', 'text', 'score', 'pub_date', 'author', 'title']
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=["title", "author"],
                message='Нельзя добавлять больше одного отзыва'
            )
        ]

class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев"""
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ["id", "text", "author", "pub_date"]
        read_only_fields = ['author']
