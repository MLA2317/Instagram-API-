from django.shortcuts import render
from .serializer import PostSerializer, PostGetSerializer, PostOtherAccountSerializer, CommentSerializer, \
    LikeGetSerializer, LikePostSerializer, CommentLikeSerializer
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Post, Comment, PostOtherAccount, CommentLike, Like


class LikeListAPI(generics.ListAPIView): # done
    queryset = Like.objects.all()
    serializer_class = LikeGetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        like = super().get_queryset()
        post_id = self.kwargs.get('post_id')
        print(post_id)
        if post_id:
            like = like.filter(post_id=post_id)
            print(like)
            return like
        return Response({'success': False, 'message': 'No such post exists'}, status=status.HTTP_404_NOT_FOUND)


class LikePostApi(generics.CreateAPIView): # done
    queryset = Like.objects.all()
    serializer_class = LikePostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['post_id'] = self.kwargs.get('post_id')
        return ctx

    def create(self, request, *args, **kwargs):
        post_id = self.kwargs.get('post_id')
        user_id = request.user
        print(user_id)
        print(user_id)
        try:
            post_id = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response({'detail': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        likes = Like.objects.filter(post_id=post_id, user_id=user_id).exists()
        if likes:
            Like.objects.filter(post_id=post_id, user_id=user_id).delete()
            return Response("Un-liked")
        instance = Like.objects.create(user_id=user_id, post_id=post_id)
        serializer = LikePostSerializer(instance)
        return Response(serializer.data)

