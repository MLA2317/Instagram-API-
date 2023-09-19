from rest_framework import serializers
from .models import Story, StoryMarkFollower, Archive


class StoryMarkFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryMarkFollower
        fields = ('story_id', 'mark')


class StorySerializer(serializers.ModelSerializer):
    #storymarkfollow = StoryMarkFollowSerializer(many=True)
    content = serializers.FileField()

    class Meta:
        model = Story
        fields = ('id', 'user_id', 'content', 'caption', 'posted')


class ArchiveSerializer(serializers.ModelSerializer):
    story = StorySerializer(read_only=True)

    class Meta:
        model = Archive
        fields = ('id', 'story', 'archived_at')

