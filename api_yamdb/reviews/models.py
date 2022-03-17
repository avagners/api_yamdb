from datetime import date

from django.core.validators import MaxValueValidator
from django.db import models
from users.models import User


class Category(models.Model):
    """Модель категорий."""
    name = models.CharField(
        max_length=256,
        unique=True
    )
    slug = models.SlugField(
        max_length=50,
        unique=True
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.slug


class Genre(models.Model):
    """Модель жанров."""
    name = models.CharField(
        max_length=256,
        unique=True
    )
    slug = models.SlugField(
        max_length=50,
        unique=True
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.slug


class Title(models.Model):
    """Модель произведений."""
    name = models.CharField(max_length=100)
    year = models.IntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(limit_value=date.today)]
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles'
    )
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'year'],
                name='unique_name_year'
            )
        ]
        ordering = ('id',)

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель отзывов."""
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique_review'
            )
        ]


class Comment(models.Model):
    """Модель комментариев."""
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments')
