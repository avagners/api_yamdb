from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    USER_ROLE = (
        ("user", "user"),
        ("moderator", "moderator"),
        ("admin", "admin"),
    )
    email = models.EmailField(max_length=254, unique=True)
    bio = models.TextField(blank=True,)
    role = models.TextField(choices=USER_ROLE, default='USER')
    confirmation_code = models.CharField(default='000000')
