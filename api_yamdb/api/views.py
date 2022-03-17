from rest_framework import viewsets, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleSerializer, UserSerializer)


class CategoryViewSet(viewsets.ModelViewSet):
    """Класс категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(viewsets.ModelViewSet):
    """Класс жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Класс произведений."""
    pass


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    pagination_class = LimitOffsetPagination
    lookup_field = 'username'
    search_fields = ('username',)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class ReviewViewSet(viewsets.ModelViewSet):
    """Получение и создание отзывов."""
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)






class CommentViewSet(viewsets.ModelViewSet):
    """Получение и создание комментариев."""
    pass
