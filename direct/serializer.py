from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import DirectMessage
from account.serializer import ProfilesSerializer


class DirectGETMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    receiver_name = serializers.SerializerMethodField()

    class Meta:
        model = DirectMessage
        fields = ('id', 'sender_name', 'receiver_name', 'message', 'file', 'is_read', 'created_date')
        extra_kwargs = {
            'post_id': {'required': False}
        }

    def get_sender_name(self, obj):
        return obj.sender.username

    def get_receiver_name(self, obj):
        return obj.receiver.username


class DirectPostMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectMessage
        fields = ('id', 'sender', 'receiver', 'message', 'file', 'is_read', 'created_date')

    def validate_sender(self, value):
        request_user = self.context['request'].user
        print('rr', request_user)
        if request_user != value:
            raise ValidationError("You can't send a message on behalf of another user")
        return value
