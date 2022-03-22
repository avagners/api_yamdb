from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class BaseAdminSettings(admin.ModelAdmin):
    """Базовая кастомизация админ панели."""
    empty_value_display = '-пусто-'
    date_hierarchy = 'pub_date'
    list_filter = ('pub_date', 'author')


class ReviewAdmin(BaseAdminSettings):
    """Кастомизация админ панели (управление отзывами)."""
    list_display = (
        'id',
        'title',
        'text',
        'author',
        'score',
        'pub_date',
    )
    list_display_links = ('id', 'text', 'score')
    search_fields = ('author', 'title')


class CommentAdmin(BaseAdminSettings):
    """Кастомизация админ панели (управление отзывами)."""
    list_display = (
        'id',
        'review',
        'text',
        'author',
        'pub_date',
    )
    list_display_links = ('id', 'text')
    search_fields = ('author', 'review')


admin.site.register(Category)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Genre)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Title)
