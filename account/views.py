from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics, serializers, status, permissions, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializer import RegisterSerializer, LoginSerializer, ProfilesSerializer, \
    FollowingListSerializer, FollowCreateSerializer, FollowerSerializer
from .models import Account, Follow
from rest_framework.parsers import MultiPartParser, FormParser


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    parser_classes = (MultiPartParser, FormParser)

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


class ProfileList(generics.ListAPIView):
    serializer_class = ProfilesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        print(user)
        queryset = Account.objects.get(id=user.id)
        print('q', queryset)
        serializer = self.serializer_class(queryset, many=False)
        print('ss', serializer)
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)


class ProfileUpdate(generics.UpdateAPIView):
    serializer_class = ProfilesSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def update(self, request, *args, **kwargs):
        user = request.user
        update = user
        serializer = self.get_serializer(update, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllAccountApi(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = ProfilesSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


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


class FollowRUD(APIView):
    serializers_class = FollowingListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk, followers, *args, **kwargs):
        try:
            follower = Follow.objects.get(following__id=pk, followers__id=followers)
            print(follower)

            follower.delete()
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


class FollowerList(APIView): #working
    serializer_class = FollowerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            queryset = Follow.objects.filter(followers=user)
            print(queryset)
        except Follow.DoesNotExist:
            return Response({'success': False, 'message': 'No following instance found for this user.'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(queryset, many=True)
        print(serializer)
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)


 # def get(self, request, account_id):
    #     try:
    #         account = Account.objects.get(id=account_id)
    #         # Assuming account has a related Follow instance
    #         followers = account.followers.all()
    #         print(followers)
    #         serializer = self.serializer_class(followers, many=True)
    #         print(serializer)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     except Account.DoesNotExist:
    #         return Response({"detail": "Account not found."}, status=status.HTTP_404_NOT_FOUND)