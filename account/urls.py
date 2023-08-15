from django.urls import path, include
from .views import RegisterAPI, LoginAPI, ProfileList, FollowingAPI, FollowingRUD, FollowerViewSet, AllAccountApi, FollowingCreate
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
    path('followings/list/', FollowingAPI.as_view()),
    path('followings/delete/<int:pk>/', FollowingRUD.as_view()),
    path('followings/create/', FollowingCreate.as_view()),
    path('followers/list/', FollowerViewSet.as_view()),

    # v1
    path('v1/', include('account.v1.urls'))
]
