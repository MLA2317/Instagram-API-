from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status, permissions
from rest_framework.decorators import action
from .models import Notification
from .serializer import NotificationSerializer


class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['GET'])
    def show_notification(self, request):
        user = request.user
        notification = Notification.objects.filter(user=user).order_by('-date')
        Notification.objects.filter(user=user, is_seen=False).update(is_seen=True)

        serializer = self.get_serializer(notification, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['DELETE'])
    def delete_notification(self, request, pk=None):
        user = request.user
        Notification.objects.filter(id=pk, user=user).delete()
        return Response(status=204)

    @action(detail=False, methods=['GET'])
    def count_notification(self, request):
        count_notifications = 0
        if request.user.is_authenticated:
            count_notifications = Notification.objects.filter(user=request.user, is_seen=False).count()
        return Response({'count_notifications': count_notifications})