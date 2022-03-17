from rest_framework import serializers
from users.models import User
from reviews.models import Category, Genre, Review, Comment, Title


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
        slug_field='username')

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
