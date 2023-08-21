from django.urls import path, include
from .views import LikeListAPI, LikePostApi, CommentListCreateApiView, CommentDeleteApiView, CommentLikeCreateAPi, PostViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('post', PostViewSet)

urlpatterns = [
    path('like-list/<int:post_id>/', LikeListAPI.as_view()),
    path('like-created/<int:post_id>/', LikePostApi.as_view()),
    path('<int:post_id>/comment/list-create', CommentListCreateApiView.as_view()),
    path('<int:pk>/comment/delete/', CommentDeleteApiView.as_view()),
    path('comment-like/create/<int:comment_id>/', CommentLikeCreateAPi.as_view()),
    path('', include(router.urls))
]
