from django.urls import path
from .view import direct_inbox, directs, senddirect, usersearch, newconversation

app_name = 'direct'

urlpatterns = [
    path('', direct_inbox, name="message"),
    path('direct/<str:username>', directs, name="directs"),
    path('send/', senddirect, name="send-directs"),
    path('search/', usersearch, name="search-users"),
    path('new/<str:username>', newconversation, name="conversation"),
]

