from django.contrib.auth.models import AbstractUser
from django.db import models


class CastomUser(AbstractUser):
    """Кастомный user"""
    class Role(models.TextChoices):
        USER = "user", "Пользователь"
        MODERATOR = "moderator", "Модератор"
        ADMIN = "admin", "Администратор"

    bio = models.TextField(blank=True, verbose_name="Биография")
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER,
        verbose_name="Роль",
    )

    class Meta():
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    @property
    def effective_role(self):
        if self.is_superuser:
            return self.Role.ADMIN
        return self.role
