from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from auch.views import signup, get_token

router = DefaultRouter()
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('genres', views.GenreViewSet, basename='genres')
router.register('titles', views.TitleViewSet, basename='titles')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', get_token, name='get_token'),
]
