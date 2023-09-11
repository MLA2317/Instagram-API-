from django.urls import path, include
from .views import SendMessageView, ListReceivedMessageView, ListSendMessageView

urlpatterns = [
    path('send-message/', SendMessageView.as_view()),
    path('message-from/', ListReceivedMessageView.as_view()),
    path('list/send-message/', ListSendMessageView.as_view()),

    #v1
    path('v1/', include('direct.v1.urls', namespace='direct'))
]
