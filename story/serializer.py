# from rest_framework import serializers
# from .models import Story, StoryMarkFollower
#
#
# class StoryMarkFollowSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = StoryMarkFollower
#         fields = ('story_id', 'mark')
#
#
# class StorySerializer(serializers.ModelSerializer):
#     StoryMarkFollow = StoryMarkFollowSerializer(many=True)
#
#     class Meta:
#         model = Story
#         fields = ('id', 'user_id', 'content', 'caption', 'StoryMarkFollow' 'posted')
#
