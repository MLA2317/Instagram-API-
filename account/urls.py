from django.urls import path, include
from .views import RegisterAPI, LoginAPI, ProfileList, FollowingList, FollowRUD, AllAccountApi, FollowCreate, FollowerList
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# routers = DefaultRouter()
# router.register(r'followers', FollowerViewSet)
# routers.register(r'followings', FollowingViewSet)


urlpatterns = [
    path('register/', RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),

    path('all_accounts/', AllAccountApi.as_view()),
    path('profile/', ProfileList.as_view()),
    path('following/list/', FollowingList.as_view()),
    path('following/unfollow/<int:pk>/users/<int:followers>/', FollowRUD.as_view()),
    path('following/create/', FollowCreate.as_view()),
    path('account/<int:account_id>/followers/list/', FollowerList.as_view()),

    # v1
    path('v1/', include('account.v1.urls'))
]
