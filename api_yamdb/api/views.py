from rest_framework import viewsets
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from .serializers import UserSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """Класс категорий."""
    pass


class GenreViewSet(viewsets.ModelViewSet):
    """Класс жанров."""
    pass


class TitleViewSet(viewsets.ModelViewSet):
    """Класс произведений."""
    pass


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
























class ReviewViewSet(viewsets.ModelViewSet):
    """Получение и создание отзывов."""
    pass







class CommentViewSet(viewsets.ModelViewSet):
    """Получение и создание комментариев."""
    pass
