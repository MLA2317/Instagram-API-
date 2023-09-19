from django.urls import path, include
from .views import RegisterAPI, LoginAPI, ProfileList, ProfileUpdate, FollowingList, FollowRUD, AllAccountApi, FollowCreate,\
    FollowerList
from rest_framework_simplejwt.views import (
     TokenObtainPairView,
     TokenRefreshView,
     TokenBlacklistView,
)
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# routers = DefaultRouter()
# router.register(r'followers', FollowerViewSet)
# routers.register(r'followings', FollowingViewSet)


urlpatterns = [
    # login, register
    path('register/', RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),

    # All profiles
    path('all_accounts/', AllAccountApi.as_view()),
    path('profile/', ProfileList.as_view()),
    path('profile/update/', ProfileUpdate.as_view()),

    # Followers
    path('following/list/', FollowingList.as_view()),
    path('<int:pk>/unfollow/<int:followers>/', FollowRUD.as_view()),
    path('following/create/', FollowCreate.as_view()),
    path('followers/list/', FollowerList.as_view()),

    # refresh token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),

    # v1
    path('v1/', include('account.v1.urls', namespace='account'))
]
