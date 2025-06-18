from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from users.views import UsersViewSet

router = DefaultRouter()
router.register("categories", views.CategoryViewSet, basename="categories")
router.register("genres", views.GenreViewSet, basename="genres")
router.register("titles", views.TitleViewSet, basename="titles")
router.register("users", UsersViewSet, basename="users")
router.register(
    r"titles/(?P<title_id>\d+)/reviews",
    views.ReviewViewSet,
    basename="reviews"
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    views.CommentViewSet,
    basename="comments"
)

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("users.urls")),
]
