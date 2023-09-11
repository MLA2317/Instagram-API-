from django.urls import path, include
from .views import LikeListAPI, LikePostApi, CommentListCreateApiView, CommentDeleteApiView,\
    PostViewSet, PostOtherAccountAPi, SaveListCreate, ExploreList
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('post', PostViewSet)
# router.register('post-other-account', PostOtherAccountAPi)

urlpatterns = [
    path('like-list/<int:post_id>/', LikeListAPI.as_view()),
    path('like-created/<int:post_id>/', LikePostApi.as_view()),
    path('<int:post_id>/comment/list-create', CommentListCreateApiView.as_view()),
    path('<int:pk>/comment/delete/', CommentDeleteApiView.as_view()),
    #path('comment-like/create/<int:comment_id>/', CommentLikeCreateAPi.as_view()),
    path('list-create/save', SaveListCreate.as_view()),
    path('explore/list', ExploreList.as_view()),
    path('', include(router.urls)),

    #v1
    path('v1/', include('post.v1.urls', namespace='post'))
]
