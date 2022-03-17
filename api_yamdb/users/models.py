from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    USER_ROLE = (
        ("USER", "user"),
        ("MODERATOR", "moderator"),
        ("ADMIN", "admin"),
    )

    email = models.EmailField(max_length=254, unique=True)
    bio = models.TextField(blank=True,)
    role = models.TextField(choices=USER_ROLE, default='USER')
    confirmation_code = models.CharField(max_length=6, default='000000')
