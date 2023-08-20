from django.urls import path
from .views import LikeListAPI, LikePostApi, CommentListCreateApiView

urlpatterns = [
    path('like-list/<int:post_id>/', LikeListAPI.as_view()),
    path('like-created/<int:post_id>/', LikePostApi.as_view()),
    path('<int:post_id>/comment/list-create', CommentListCreateApiView.as_view())
]
