from rest_framework import viewsets, filters, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from .permissions import AuthorOrAuthenticatedReadOnly
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleSerializer, UserSerializer,
                          SendConfirmationCodeSerializer)
from django.core.mail import send_mail
import random
from rest_framework.response import Response


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
    permission_class = (AllowAny,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Получение и создание комментариев."""
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    permission_class = (AllowAny,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        review = title.reviews.all().get(pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class SendConfirmationCodeView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SendConfirmationCodeSerializer(data=request.data)
        email = request.data.get('email')
        username = request.data.get('username')

        if serializer.is_valid():
            confirmation_code = ''.join(map(str, random.sample(range(10), 6)))

            user = User.objects.filter(email=email).exists()
            if not user:
                User.objects.create_user(email=email, username=username)
            User.objects.filter(email=email).update(
                confirmation_code=confirmation_code
            )
            send_mail(
                subject='Ваш код подтверждения',
                message=f'Ваш код подтверждения: {confirmation_code}',
                from_email='confirmation@yambd.com',
                recipient_list=[email],
                fail_silently=False,
            )
            return Response(f'Код подтверждения отправлен на адрес {email}',
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
