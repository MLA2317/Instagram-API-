from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationList, NotificationDelete

urlpatterns = [
    path('notification/list', NotificationList.as_view()),
    path('notification/delete/<int:pk>/', NotificationDelete.as_view()),

    #v1
    path('v1/', include('notification.v1.urls', namespace='notification'))
]