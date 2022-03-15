from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


class User(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True,
    )
    bio = models.TextField(
        "Биография",
        blank=True,
    )
    role = models.TextField(
        "Пользовательская роль",
        choices=UserRole.choices,
        default=UserRole.USER,
    )
