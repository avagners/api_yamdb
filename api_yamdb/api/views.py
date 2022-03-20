from rest_framework import viewsets, filters, status
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from .mixins import ListCreateDestroyViewSet
from .permissions import (AuthorOrAuthenticatedReadOnly,
                          IsAdminOrReadOnly, IsAdmin, IsSuperUser)
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, UpdateSelfSerializer,
                          ReviewSerializer,
                          TitleSerializer, UserSerializer,
                          SendConfirmationCodeSerializer, SendTokenSerializer)
from django.core.mail import send_mail
import random
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import action


class CategoryViewSet(ListCreateDestroyViewSet):
    """Класс категорий."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(ListCreateDestroyViewSet):
    """Класс жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """Класс произведений."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'year', 'category', 'genre')


class UserViewSet(viewsets.ModelViewSet):
    """Класс пользователей."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin, IsSuperUser)
    filter_backends = (filters.SearchFilter,)
    pagination_class = LimitOffsetPagination
    lookup_field = 'username'
    search_fields = ('username',)

    @action(detail=False, methods=['get', 'patch'],
            url_path='me', permission_classes=[IsAuthenticated])
    def get_or_update_self(self, request):
        """
        Функция обрабатывает 'GET' и 'PATCH' запросы на эндпоинт '/users/me/'
        """
        if request.method != 'GET':
            serializer = UpdateSelfSerializer(
                instance=request.user, data=request.data
            )
            serializer.is_valid(raise_exception=True)

            email = request.data.get('email')
            username = request.data.get('username')
            user_email = User.objects.filter(email=email).exists()
            user_username = User.objects.filter(username=username).exists()

            data_of_me = self.get_serializer(request.user, many=False)

            if user_email and email != data_of_me.data.get('email'):
                message = {'email': f'{email} уже зарегистрирован'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            elif user_username and username != data_of_me.data.get('username'):
                message = {'username': f'{username} уже зарегистрирован'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data)
        else:
            serializer = self.get_serializer(request.user, many=False)
            return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        "Функция переопределяет 'PATCH-запрос' на 'PUT'"
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
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        review = title.reviews.all().get(pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


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
