from django.db.models import Avg
from rest_framework import viewsets, mixins, filters
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Category, Genre, Review, Title
from api.permissions import (IsAdminOrReadOnly,
                             IsAuthorOrModeratorOrAdminOrReadOnly)
from .serializers import (CategorySerializer,
                          CommentSerializer,
                          GenreSerializer,
                          ReviewSerializer,
                          TitleReadSerializer,
                          TitleWriteSerializer)


class CategoryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Категории"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class GenreViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Жанры"""
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)

    def get_queryset(self):
        queryset = Genre.objects.all()
        name = self.request.query_params.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class TitleViewSet(viewsets.ModelViewSet):
    """Произведения"""
    permission_classes = [IsAdminOrReadOnly]
    http_method_names = ["get", "patch", "post", "delete"]

    def get_queryset(self):
        queryset = Title.objects.all().annotate(
            rating=Avg("reviews__score")
        )

        category_slug = self.request.query_params.get("category")
        genre_slug = self.request.query_params.get("genre")
        name = self.request.query_params.get("name")
        year = self.request.query_params.get("year")

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        if genre_slug:
            queryset = queryset.filter(genre__slug=genre_slug)
        if name:
            queryset = queryset.filter(name__icontains=name)
        if year:
            queryset = queryset.filter(year=year)

        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Отзывы"""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrModeratorOrAdminOrReadOnly,)
    http_method_names = ["get", "patch", "post", "delete"]
    pagination_class = LimitOffsetPagination

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get("title_id"))

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=serializer.context['title'])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['title'] = self.get_title()
        return context


class CommentViewSet(viewsets.ModelViewSet):
    """Комментарии"""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrModeratorOrAdminOrReadOnly,)
    http_method_names = ["get", "patch", "post", "delete"]
    pagination_class = LimitOffsetPagination

    def get_review(self):
        title_id = self.kwargs.get("title_id")
        review_id = self.kwargs.get("review_id")
        if title_id:
            return get_object_or_404(
                Review,
                id=review_id,
                title=title_id
            )
        return get_object_or_404(
            Review,
            id=review_id,
        )

    def get_queryset(self):
        review = self.get_review()
        # review = self.get_review(self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)
