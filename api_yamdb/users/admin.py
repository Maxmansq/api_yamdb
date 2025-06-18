from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CastomUser


UserAdmin.fieldsets += (
    ("Дополнительные данные о пользователе", {"fields": ("bio", "role",)}),
)

admin.site.register(CastomUser, UserAdmin)
