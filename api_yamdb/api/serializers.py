from django.core.validators import MaxValueValidator
from django.db.models import Avg
from django.utils import timezone
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id',
                  'name',
                  'year',
                  'rating',
                  'description',
                  'genre',
                  'category',)

    def get_rating(self, obj):
        return obj.reviews.aggregate(rating=Avg('score')).get('rating')


class TitlePostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True, slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    year = serializers.IntegerField(validators=(MaxValueValidator(
        timezone.now().year,
        message='Год не может быть больше текущего!'),))

    class Meta:
        model = Title
        fields = ('id',
                  'name',
                  'year',
                  'description',
                  'genre',
                  'category',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        ref_name = 'ReadOnlyUsers'


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели отзывов."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate_score(self, value):
        score = [i for i in range(1, 11)]
        if value not in score:
            raise serializers.ValidationError(
                'Оценка должна быть в диапазоне 1-10.'
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username')

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class SendConfirmationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)


class SendTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(
        required=True,
    )


class UpdateSelfSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio'
        )
