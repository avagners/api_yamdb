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
                          SendConfirmationCodeSerializer, SendTokenSerializer)
from django.core.mail import send_mail
import random
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken


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
    permission_class = (AuthorOrAuthenticatedReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Получение и создание комментариев."""
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    permission_class = (AuthorOrAuthenticatedReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        review = title.reviews.all().get(pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class SendConfirmationCodeView(APIView):
    """
    Вью-класс описывает POST-запрос для регистрации нового пользователя и
    получаения кода подтверждения, который необходим для получения JWT-токена.

    На вход подается 'username' и 'email', а в ответ происходит отправка
    на почту письма с кодом подтверждения.
    """
    permission_classes = (AllowAny,)

    @staticmethod
    def send_email(email):
        confirmation_code = ''.join(map(str, random.sample(range(10), 6)))
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

    def post(self, request):
        serializer = SendConfirmationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = request.data.get('email')
        username = request.data.get('username')
        user_email = User.objects.filter(email=email).exists()
        user_username = User.objects.filter(username=username).exists()

        if user_email:
            message = {'email': f'{email} уже зарегистрирован. '
                       f'На {email} отправлен код для получения токена.'}
            self.send_email(email)
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        elif user_username:
            message = {'username': f'{username} уже зарегистрирован. '
                       f'На {email} отправлен код для получения токена.'}
            self.send_email(email)
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        elif username == 'me':
            message = {'username': f'Некорректный username = "{username}"'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        elif not (user_email or user_username):
            User.objects.create_user(email=email, username=username)
            self.send_email(email)
            message = {'email': email, 'username': username}
            return Response(message, status=status.HTTP_200_OK)


class SendTokenView(APIView):
    """
    Вью-класс описывает POST-запрос для получаения JWT-токена.

    На вход подается 'username' и 'confirmation_code',
    а в ответ формируется JWT-токен.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SendTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.data.get('username')
        user = get_object_or_404(User, username=username)
        if user.confirmation_code != request.data.get('confirmation_code'):
            message = {'confirmation_code': 'Неверный код подтверждения'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        message = {'token': str(AccessToken.for_user(user))}
        return Response(message, status=status.HTTP_200_OK)
