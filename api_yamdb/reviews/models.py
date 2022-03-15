from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True
    )

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        max_length=50,
        unique=True)

    def __str__(self):
        return self.slug
