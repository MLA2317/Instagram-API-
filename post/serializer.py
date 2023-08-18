from rest_framework import serializers
from .models import Post, PostOtherAccount, Like, Comment, CommentLike
from account.serializer import AccountListSerializer


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


class CommentSerializer(serializers.ModelSerializer):
    user_id = AccountListSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'user_id', 'post_id', 'message', 'created_date')
        extra_kwargs = {
            'author': {'read_only': True}
        }


class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = ('id', 'user_id', 'comment_id')


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

    @staticmethod
    def get_likes_count(obj):
        return obj.like.count()

    @staticmethod
    def get_comment_count(obj):
        return obj.comment.count()


class PostOtherAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostOtherAccount
        fields = ('id', 'post_id', 'users_id')
