from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from .models import Notification
from .serializer import NotificationSerializer


class NotificationList(APIView):
    # queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        notification = self.get_queryset()
        serializer = self.serializer_class(notification, many=True)
        return Response(serializer.data)


class NotificationDelete(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Notification.objects.get(pk=pk, user=self.request.user)
        except Notification.DoesNotExist:
            raise NotFound('Notification Not Found')

    def delete(self, request, pk, *args, **kwargs):
        notification = self.get_object(pk)
        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



    # @action(detail=False, methods=['GET'])
    # def show_notification(self, request):
    #     user = request.user
    #     notification = Notification.objects.filter(user=user).order_by('-date')
    #     Notification.objects.filter(user=user, is_seen=False).update(is_seen=True)
    #
    #     serializer = self.get_serializer(notification, many=True)
    #     return Response(serializer.data)
    #
    # @action(detail=True, methods=['DELETE'])
    # def delete_notification(self, request, pk=None):
    #     user = request.user
    #     Notification.objects.filter(id=pk, user=user).delete()
    #     return Response(status=204)
    #
    # @action(detail=False, methods=['GET'])
    # def count_notification(self, request):
    #     count_notifications = 0
    #     if request.user.is_authenticated:
    #         count_notifications = Notification.objects.filter(user=request.user, is_seen=False).count()
    #     return Response({'count_notifications': count_notifications})