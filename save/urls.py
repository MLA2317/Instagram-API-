from django.urls import path, include
from .views import SaveListCreate

urlpatterns = [
    path('list-create/', SaveListCreate.as_view())
]

