from django.urls import path, include
from .views import RegisterAPI, LoginAPI, ProfileList, FollowingViewSet, FollowerViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
routers = DefaultRouter()
router.register(r'followers', FollowerViewSet)
routers.register(r'followings', FollowingViewSet)


urlpatterns = [
    path('register/', RegisterAPI.as_view()),
    path('login/', LoginAPI.as_view()),

    path('profile/', ProfileList.as_view()),
    path('followings/', include(router.urls)),
    path('followers/', include(routers.urls))
]
