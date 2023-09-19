from rest_framework import serializers
from .models import Post, Like, Comment, Save
from account.serializer import ProfilesSerializer, AccountListSerializer
from django_countries.serializer_fields import CountryField


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
    #parent_comment = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), required=False, default=None, allow_null=True)
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
            'top_level_comment_id': {'read_only': True},
            'post_id': {'read_only': True},
        }

    def create(self, validated_data):  # done
        request = self.context['request']
        post_id = Post.objects.get(id=self.context['post_id'])
        user_id = request.user
        print('user', user_id)
        instance = Comment.objects.create(user_id=user_id, post_id=post_id, **validated_data)
        print('instance', instance)
        return instance


class PostDetailSerializer(serializers.ModelSerializer): # Done
    likes_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'user_id', 'image', 'description', 'likes_count', 'comment_count',
                  'created_date', 'update_date')

    def get_likes_count(self, obj):
        return Like.objects.filter(post_id=obj.id).count()

    def get_comment_count(self, obj):
        return Comment.objects.filter(post_id=obj.id).count()


class PostSerializer(serializers.ModelSerializer): # Done
    image = serializers.FileField()

    class Meta:
        model = Post
        fields = ('id', 'user_id', 'image', 'description', 'created_date')


class SaveSerializer(serializers.ModelSerializer):
    #posts = PostSerializer(many=True)

    class Meta:
        model = Save
        fields = ('id', 'account_id', 'posts')


class ExploreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'user_id', 'image')



