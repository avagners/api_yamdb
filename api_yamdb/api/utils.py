from django.shortcuts import get_object_or_404
from reviews.models import Title


def get_reviews_obj(obj, title_obj_id, review_obj_id):
    """Получение объектов отзывов."""
    title = get_object_or_404(Title, pk=obj.kwargs.get(title_obj_id))
    return title.reviews.all().get(pk=obj.kwargs.get(review_obj_id))


def get_titles_obj(obj, title_id):
    """Получение объектов произведений."""
    return get_object_or_404(Title, pk=obj.kwargs.get(title_id))
