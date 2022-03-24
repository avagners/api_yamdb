from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole:
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    choices = [
        (USER, 'user'),
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
    ]


class User(AbstractUser):
    """Модель пользователей."""
    email = models.EmailField(max_length=254, unique=True)
    bio = models.TextField(blank=True,)
    role = models.TextField(choices=UserRole.choices, default=UserRole.USER)
    confirmation_code = models.TextField(default='000000')
