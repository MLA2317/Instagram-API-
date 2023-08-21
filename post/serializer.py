from rest_framework import serializers
from .models import Post, PostOtherAccount, Like, Comment, CommentLike
from account.serializer import ProfilesSerializer, AccountListSerializer


class LikeGetSerializer(serializers.ModelSerializer): # done
    user_id = AccountListSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ('id', 'user_id', 'post_id',)
        # extra_kwargs = {
        #     'author': {'read_only': True}
        # }


class LikePostSerializer(serializers.ModelSerializer): # done
    class Meta:
        model = Like
        fields = ('post_id',)
        extra_kwargs = {
            'user_id': {'required': False},
            'post_id': {'required': False}
        }


class MiniCommentSerializer(serializers.ModelSerializer): # Done
    class Meta:
        model = Comment
        fields = ('id', 'user_id', 'post_id', 'parent_comment', 'message', 'top_level_comment_id', 'created_date')


class CommentSerializer(serializers.ModelSerializer):
    user_id = ProfilesSerializer(read_only=True)
    children = serializers.SerializerMethodField(read_only=True)

    def get_children(self, obj):
        children = Comment.objects.filter(parent_comment_id=obj.id)
        serializer = MiniCommentSerializer(children, many=True)
        return serializer.data

    class Meta:
        model = Comment
        fields = ('id', 'user_id', 'post_id',  'parent_comment', 'message',  'top_level_comment_id', 'children', 'created_date')
        extra_kwargs = {
            'user_id': {'read_only': True},
            'post_id': {'read_only': True},
            'top_level_comment_id': {'read_only': True}
        }

    def create(self, validated_data):  # done
        request = self.context['request']
        post_id = self.context['post_id']
        user_id = request.user.id
        instance = Comment.objects.create(user_id=user_id, post_id=post_id, **validated_data)
        return instance


class CommentLikeSerializer(serializers.ModelSerializer): #done
    class Meta:
        model = CommentLike
        fields = ('comment_id',)
        extra_kwargs = {
            'user_id': {'required': False},
            'comment_id': {'required': False}
        }


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'user_id', 'image', 'location', 'description', 'archieve', 'send', 'created_date', 'modified_date')


class PostGetSerializer(serializers.ModelSerializer):
    like = LikeGetSerializer(many=True, read_only=True)
    like_count = serializers.SerializerMethodField("get_likes_count")
    comment = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField('get_comment_count')
    user_id = AccountListSerializer(read_only=True)
    comment_like = CommentLikeSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'user_id', 'image', 'location', 'description', 'like', 'like_count', 'comment', 'comment_count', 'comment_like')


class PostOtherAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostOtherAccount
        fields = ('id', 'post_id', 'users_id')
