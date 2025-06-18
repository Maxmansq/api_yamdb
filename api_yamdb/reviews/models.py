from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.conf import settings

from core.models import SlugNameModel

MAX_SCORE = 10
MIN_SCORE = 1


class Review(models.Model):
    """Отзывы"""
    title = models.ForeignKey(
        "Title",
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Заголовок",
    )
    text = models.TextField(verbose_name="Текст")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор",
    )
    score = models.PositiveSmallIntegerField(
        verbose_name="Оценка",
        validators=[
            MaxValueValidator(MAX_SCORE),
            MinValueValidator(MIN_SCORE)
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания")

    class Meta:
        ordering = ["-pub_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author"],
                name="unique_review"
            )
        ]

    def __str__(self):
        return f"Review by {self.author} for {self.title}"


class Category(SlugNameModel):
    """Категории"""

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Genre(SlugNameModel):
    """Жанры"""

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произвадения"""
    name = models.CharField(max_length=256, verbose_name="Название")
    year = models.PositiveSmallIntegerField(verbose_name="Год")
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(
        Genre,
        related_name="titles",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="titles"
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Comment(models.Model):
    """Комментарии"""
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания")

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self):
        return (f"Коментарий от {self.author}")
