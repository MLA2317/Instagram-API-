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


class CommentSerializer(serializers.ModelSerializer): # Done
    #user_id = ProfilesSerializer(read_only=True)
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
        post = Post.objects.get(id=self.context['post_id'])
        user = request.user
        instance = Comment.objects.create(user_id=user, post_id=post, **validated_data)
        return instance


class CommentLikeSerializer(serializers.ModelSerializer): #done
    class Meta:
        model = CommentLike
        fields = ('comment_id',)
        extra_kwargs = {
            'user_id': {'required': False},
            'comment_id': {'required': False}
        }


class PostDetailSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'user_id', 'image', 'location', 'description', 'archive', 'send', 'likes_count', 'comment_count',
                  'created_date', 'update_date')

    def get_likes_count(self, obj):
        return Like.objects.filter(post_id=obj.id).count()

    def get_comment_count(self, obj):
        return Comment.objects.filter(post_id=obj.id).count()


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'user_id', 'image', 'location', 'description', 'archive', 'send')


class PostOtherAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostOtherAccount
        fields = ('id', 'post_id', 'users_id')
