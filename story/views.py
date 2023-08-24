from django.shortcuts import render
from .serializer import StorySerializer
from rest_framework import generics, permissions
from .models import Story


class StoryListCreate(generics.ListCreateAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = [permissions.IsAuthenticated]

    # def create(self, request, *args, **kwargs):
