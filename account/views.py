from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics, serializers, status, permissions, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializer import RegisterSerializer, LoginSerializer, LocationSerializer, ProfilesSerializer, \
    FollowingListSerializer, FollowCreateSerializer, FollowerSerializer
from .models import Account, Location, Follow


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success': True, 'data': 'Account successfully created'}, status=status.HTTP_201_CREATED)


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'tokens': serializer.data['tokens']}, status=status.HTTP_200_OK)


class LocationListCreate(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProfileList(generics.ListAPIView):
    serializer_class = ProfilesSerializer
    permissions = IsAuthenticated

    def get(self, request, *args, **kwargs):
        user = request.user
        print(user)
        queryset = Account.objects.get(id=user.id)
        serializer = self.serializer_class(queryset)
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)


class AllAccountApi(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = ProfilesSerializer
    permissions = IsAuthenticated


class FollowingList(APIView):
    serializer_class = FollowingListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            queryset = Follow.objects.filter(following=user)
            print(queryset)
        except Follow.DoesNotExist:
            return Response({'success': False, 'message': 'No following instance found for this user.'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(queryset, many=True)
        print(serializer)
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)


# class FollowRUD(APIView):
#     serializers_class = FollowingListSerializer
#
#     def delete(self, request, pk, followers, *args, **kwargs):
#         following = Follow.objects.filter(following__account_following=pk)
#
#         if not following.exists():
#             return Response({"detail": "Following record not found for the given following_user id"},
#                             status=status.HTTP_404_NOT_FOUND)
#
#         # Operate on the first instance for now
#         following = following.first()
#         print(following)
#         #
#         # user_to_unfollow = following.followers.filter(id=followers).first()
#         # print(user_to_unfollow)
#
#         if following.followers.id == followers:
#             user_to_unfollow = following.followers
#         else:
#             user_to_unfollow = None
#
#         if not user_to_unfollow:
#             return Response({"detail": "User not found in the following list of the specified following_user"},
#                             status=status.HTTP_404_NOT_FOUND)
#
#         if user_to_unfollow == following.followers:
#             following.delete()
#         print(following)
#         return Response({"detail": "Unfollowed successfully"}, status=status.HTTP_204_NO_CONTENT)

#
class FollowRUD(APIView):
    serializers_class = FollowingListSerializer

    def delete(self, request, pk, followers, *args, **kwargs):
        try:
            # Find the Follow relationship instance where the user is following another user
            following_instance = Follow.objects.get(following__id=pk, followers__id=followers)
            print(following_instance)

            # Delete the found relationship to "unfollow" the user
            following_instance.delete()
            return Response({"detail": "Unfollowed successfully"}, status=status.HTTP_204_NO_CONTENT)

        except Follow.DoesNotExist:
            return Response({"detail": "Following relationship not found for the given IDs"},
                            status=status.HTTP_404_NOT_FOUND)


class FollowCreate(generics.CreateAPIView):
    serializer_class = FollowCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        following = request.user
        followers_ids = request.data.get('followers', [])

        if not isinstance(followers_ids, list):
            followers_ids = [followers_ids]

        if following.id in followers_ids:
            return Response({'success': False, 'message': "Siz ozizga oziz follow qila olmaysiz"},
                            status=status.HTTP_400_BAD_REQUEST)

        for follower_id in followers_ids:
            try:
                Account.objects.get(id=follower_id)
            except Account.DoesNotExist:
                return Response({'success': False, 'message': "Bunday foydalanuvchi mavjud emas"},
                                status=status.HTTP_404_NOT_FOUND)

        # Check if you're already following these users
        already_following = Follow.objects.filter(following=following, followers__id__in=followers_ids)
        if already_following.exists():
            return Response({'success': False, 'message': 'Siz allaqachon bu foydalanuvchini follow qilgansiz'},
                            status=status.HTTP_400_BAD_REQUEST)

        followed_users = []
        for follower_id in followers_ids:
            follow_instance, created = Follow.objects.get_or_create(following=following, followers_id=follower_id)
            if created:
                followed_users.append(follow_instance)

        serializer = self.serializer_class(followed_users, many=True)
        return Response({'success': True, 'message': 'Successfully followed the user(s)', 'data': serializer.data},
                        status=status.HTTP_201_CREATED)


class FollowerList(APIView): # not working

    def get(self, request, account_id):
        try:
            account = Account.objects.get(id=account_id)
            # Assuming account has a related Follow instance
            followers = account.followers.all()
            print(followers)
            serializer = FollowerSerializer(followers, many=True)
            print(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response({"detail": "Account not found."}, status=status.HTTP_404_NOT_FOUND)


