from django.urls import path
from .view import register
from django.contrib.auth import views


# app_name = 'account'

urlpatterns = [
    path('register/', register, name='sign-up'),
    path('login/', views.LoginView.as_view(template_name='register/login.html'), name='sign-in'), #redirect_authenticated_user=True
    path('logout/', views.LogoutView.as_view(template_name='register/logout.html'), name='sign-out')

]
