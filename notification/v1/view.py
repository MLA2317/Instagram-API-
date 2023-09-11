from django.shortcuts import render, redirect
from notification.models import Notification


def ShowNotification(request):
    user = request.user
    notification = Notification.objects.filter(user=user).order_by('-date')
    Notification.objects.filter(user=user, is_seen=False).update(is_seen=True)

    ctx = {
        'notifications': notification
    }
    return render(request, 'notification/notification.html', ctx)


def DeleteNotification(request, pk):
    user = request.user
    Notification.objects.filter(id=pk, user=user).delete()
    return redirect('show_notification:show-notification')
