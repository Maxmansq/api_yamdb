from django.db import models


class SlugNameModel(models.Model):
    name = models.CharField(max_length=256, verbose_name="Название")
    slug = models.SlugField(max_length=50, unique=True, verbose_name="Слаг")

    class Meta:
        abstract = True
