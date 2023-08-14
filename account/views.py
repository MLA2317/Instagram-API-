from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics, serializers, status, permissions, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializer import RegisterSerializer, LoginSerializer, LocationSerializer, ProfilesSerializer, \
    FollowerSerializer, FollowingSerializer, AllAccountsSerializer
from .models import Account, Location, Follower, Following


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
    serializer_class = AllAccountsSerializer
    permissions = IsAuthenticated


class FollowingViewSet(viewsets.ModelViewSet):
    queryset = Following.objects.all()
    serializer_class = FollowingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()


class FollowerViewSet(viewsets.ModelViewSet):
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()
