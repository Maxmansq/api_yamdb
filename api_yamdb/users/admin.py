from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import MyUser



UserAdmin.fieldsets += (
    # Добавляем кортеж, где первый элемент — это название раздела в админке,
    # а второй элемент — словарь, где под ключом fields можно указать нужные поля.
    ('Дополнительные данные о пользователе', {'fields': ('bio', 'role',)}),
)

admin.site.register(MyUser, UserAdmin)
