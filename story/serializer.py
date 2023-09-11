from rest_framework import serializers
from .models import Story, StoryMarkFollower, Archive


class StoryMarkFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryMarkFollower
        fields = ('story_id', 'mark')


class StorySerializer(serializers.ModelSerializer):
    #storymarkfollow = StoryMarkFollowSerializer(many=True)

    class Meta:
        model = Story
        fields = ('id', 'user_id', 'content', 'caption', 'posted')


class ArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Archive
        fields = ('id', 'story', 'user_id', 'content', 'archived_at')

