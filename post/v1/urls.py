from django.urls import path
from .view import index, new_post, PostDetail, like, explore, saves

app_name = 'post'

urlpatterns = [
    path('', index, name='index'),
    path('newpost/', new_post, name='newpost'),
    path('detail/<int:pk>/', PostDetail.as_view(), name='detail'),
    path('<int:post_id>/like/', like, name='like'),
    path('explore/', explore, name='explore'),
    path('save/<int:post_id>/', saves, name='saves'),
]
