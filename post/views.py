# from django.shortcuts import render
# from .serializer import PostSerializer, PostDetailSerializer, PostOtherAccountSerializer, CommentSerializer, \
#     LikeGetSerializer, LikePostSerializer, CommentLikeSerializer
# from rest_framework import generics, status, permissions, viewsets
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated, IsAdminUser
# from .models import Post, Comment, PostOtherAccount, CommentLike, Like
#
#
# class LikeListAPI(generics.ListAPIView): # done
#     queryset = Like.objects.all()
#     serializer_class = LikeGetSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_queryset(self, *args, **kwargs):
#         like = super().get_queryset()
#         post_id = self.kwargs.get('post_id')
#         print(post_id)
#         if post_id:
#             like = like.filter(post_id=post_id)
#             print(like)
#             return like
#         return Response({'success': False, 'message': 'No such post exists'}, status=status.HTTP_404_NOT_FOUND)
#
#
# class LikePostApi(generics.CreateAPIView): # done
#     queryset = Like.objects.all()
#     serializer_class = LikePostSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_serializer_context(self):
#         ctx = super().get_serializer_context()
#         ctx['post_id'] = self.kwargs.get('post_id')
#         return ctx
#
#     def create(self, request, *args, **kwargs):
#         post_id = self.kwargs.get('post_id')
#         user_id = request.user
#         print(user_id)
#         try:
#             post_id = Post.objects.get(pk=post_id)
#         except Post.DoesNotExist:
#             return Response({'detail': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
#         likes = Like.objects.filter(post_id=post_id, user_id=user_id).exists()
#         if likes:
#             Like.objects.filter(post_id=post_id, user_id=user_id).delete()
#             return Response("Un-liked")
#         instance = Like.objects.create(user_id=user_id, post_id=post_id)
#         serializer = LikePostSerializer(instance)
#         return Response(serializer.data)
#
#
# class CommentListCreateApiView(generics.ListCreateAPIView): # Done
#     queryset = Comment.objects.filter(parent_comment__isnull=True)
#     serializer_class = CommentSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#
#     def get_serializer_context(self):
#         ctx = super().get_serializer_context()
#         ctx['post_id'] = self.kwargs.get('post_id')
#         return ctx
#
#     def get_queryset(self):
#         qs = super().get_queryset()
#         post_id = self.kwargs.get('post_id')
#         qs = qs.filter(post_id=post_id)
#         return qs
#
#
# class CommentDeleteApiView(APIView): # Done
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#
#     def get_object(self, pk):
#         try:
#             return Comment.objects.get(pk=pk)
#         except Comment.DoesNotExist:
#             return None
#
#     def delete(self, request, pk, *args, **kwargs):
#         comment = self.get_object(pk)
#         print(comment)
#
#         if comment is None:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#
#         if comment.user_id != request.user:
#             return Response(status=status.HTTP_403_FORBIDDEN)
#
#         comment.delete()
#         print('delete', comment)
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# class CommentLikeCreateAPi(generics.CreateAPIView): # Done
#     queryset = CommentLike.objects.all()
#     serializer_class = CommentLikeSerializer
#
#     def get_serializer_context(self):
#         ctx = super().get_serializer_context()
#         ctx['comment_id'] = self.kwargs.get('comment_id')
#         return ctx
#
#     def create(self, request, *args, **kwargs):
#         comment_id = self.kwargs.get('comment_id')
#         user_id = request.user
#         print(user_id)
#         try:
#             comment_id = Comment.objects.get(pk=comment_id)
#         except Comment.DoesNotExist:
#             return Response({'detail': 'Comment NOT Found!'}, status=status.HTTP_404_NOT_FOUND)
#         comment_likes = CommentLike.objects.filter(comment_id=comment_id, user_id=user_id).exists()
#         if comment_likes:
#             CommentLike.objects.filter(comment_id=comment_id, user_id=user_id).delete()
#             return Response('Un-like comment')
#
#         instance = CommentLike.objects.create(user_id=user_id, comment_id=comment_id)
#         serializer = CommentLikeSerializer(instance)
#         return Response(serializer.data)
#
#
# class PostViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#
#     # for user.id belong to posts
#     def get_queryset(self):
#         return Post.objects.filter(user_id=self.request.user.id)
#
#     def get_serializer_class(self):
#         if self.action in ['create']:
#             return PostSerializer
#         return PostDetailSerializer
#
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         if instance.user_id != request.user.id:
#             return Response({'detail': "Not found"}, status=status.HTTP_404_NOT_FOUND)
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)
#
#
# class PostOtherAccountAPi(viewsets.ModelViewSet):
#     queryset = PostOtherAccount.objects.all()
#     serializer_class = PostOtherAccountSerializer
#
#     def retrieve(self, request, *args, **kwargs):
#         post_other_account = self.get_object()
#         serializer = PostOtherAccountSerializer(post_other_account)
#         return Response(serializer.data)
