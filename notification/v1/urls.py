from django.urls import path
from .view import ShowNotification, DeleteNotification

app_name = 'notification'

urlpatterns = [
    path('show-notification/', ShowNotification, name='show-notification'),
    path('notification/<int:pk>/', DeleteNotification, name='delete-notification')
]

