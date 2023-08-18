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
        return Response(serializer.data, status=status.HTTP_200_OK)


class LocationListCreate(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


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
            queryset = Follow.objects.get(following=user)
            print(queryset)
        except Follow.DoesNotExist:
            return Response({'success': False, 'message': 'No following instance found for this user.'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(queryset)
        print(serializer)
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)


class FollowRUD(APIView):
    serializers_class = FollowingListSerializer

    def delete(self, request, pk, followers, *args, **kwargs):
        try:
            following_instance = Follow.objects.get(following__account_following=pk)
            print(following_instance)

            # `users_id` many-to-many field dagi kerakli foydalanuvchini qidirish
            user_to_unfollow = following_instance.followers.filter(id=followers).first()
            print(user_to_unfollow)

            if not user_to_unfollow:
                return Response({"detail": "User not found in the following list of the specified following_user"},
                                status=status.HTTP_404_NOT_FOUND)

            following_instance.followers.remove(user_to_unfollow)
            print(following_instance)
            return Response({"detail": "Unfollowed successfully"}, status=status.HTTP_204_NO_CONTENT)

        except Follow.DoesNotExist:
            return Response({"detail": "Following record not found for the given following_user id"},
                            status=status.HTTP_404_NOT_FOUND)


class FollowCreate(generics.CreateAPIView):
    serializer_class = FollowCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        following = request.user
        followers = request.data.get('followers')

        if not followers:
            return Response({'success': False, 'message': 'User ID to follow is required'},
                            status=status.HTTP_400_BAD_REQUEST)

        if following.id in followers:
            return Response({'success': False, 'message': "You can't follow yourself!"},
                            status=status.HTTP_400_BAD_REQUEST)

            # Check if you're already following these users
        already_following = Follow.objects.filter(following_id=following.id, followers__in=followers)
        if already_following.exists():
            return Response({'success': False, 'message': 'You already follow one or more of these users'},
                            status=status.HTTP_400_BAD_REQUEST)

        following_instance, created = Follow.objects.get_or_create(following_id=following)
        if created:
            # If the instance was just created, add the users to the users_id field
            following_instance.followers.add(*followers)
        else:
            # If the instance already existed, we need to ensure that adding these users won't cause duplicates
            for user_id in followers:
                if not following_instance.followers.filter(id=user_id).exists():
                    following_instance.followers.add(user_id)

        serializer = self.serializer_class(following_instance)
        return Response({'success': True, 'message': 'Successfully followed the user(s)', 'data': serializer.data},
                        status=status.HTTP_201_CREATED)


class FollowerList(APIView): # not working
    def get(self, request, account_id):
        try:
            account = Account.objects.get(id=account_id)
            # Assuming account has a related Follow instance
            follow_instance = account.followers.all()
            print(follow_instance)
            serializer = FollowerSerializer(follow_instance)
            print(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response({"detail": "Account not found."}, status=status.HTTP_404_NOT_FOUND)


