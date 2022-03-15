from rest_framework import viewsets
from reviews.models import Review, Comment



























class ReviewViewSet(viewsets.ModelViewSet):
    """Получение и создание отзывов."""
    pass







class CommentViewSet(viewsets.ModelViewSet):
    """Получение и создание комментариев."""
    pass
