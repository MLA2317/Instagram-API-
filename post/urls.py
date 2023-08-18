from django.urls import path
from .views import LikeListAPI, LikePostApi

urlpatterns = [
    path('like-list/<int:post_id>/', LikeListAPI.as_view()),
    path('like-created/<int:post_id>/', LikePostApi.as_view()),
]
