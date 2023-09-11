from django.urls import path
from .view import Register, profile, EditProfile, Login, logout_view, follow

app_name = 'v1'

urlpatterns = [
    path('register/', Register.as_view(), name='sign-up'),
    path('login/', Login.as_view(),  name='sign-in'), #redirect_authenticated_user=True
    path('logout/', logout_view, name='sign-out'),

    path('profile/<str:username>/', profile, name='profile'),
    path('edit/', EditProfile, name='editprofile'),

    path('follow/<str:username>/<int:option>/', follow, name='follow')

    # path('following/', following, name='following')

]
