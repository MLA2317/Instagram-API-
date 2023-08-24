from django.urls import path
from .view import index

urlpatterns = [
    path('', index, name='index')
]