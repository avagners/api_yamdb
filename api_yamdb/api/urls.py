from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from .views import CategoryViewSet, GenreViewSet, TitleViewSet

router = routers.DefaultRouter()

router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register('titles', TitleViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/api-token-auth/', views.obtain_auth_token),
]