from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'post', 'sender', 'user', 'notification_type', 'text_preview', 'date', 'is_seen')
