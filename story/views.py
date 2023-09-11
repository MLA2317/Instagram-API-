from django.shortcuts import render
from .serializer import StorySerializer, ArchiveSerializer
from rest_framework import generics, permissions
from .models import Story, Archive
from .permission import IsOwnerOrAdmin


class StoryListCreate(generics.ListCreateAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = [permissions.IsAuthenticated]


class StoryDestroy(generics.DestroyAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def perform_destroy(self, instance):
        instance.delete()


class ArchiveList(generics.ListAPIView):
    queryset = Archive.objects.all().order_by('-archived_at')
    serializer_class = ArchiveSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Archive.objects.filter(user_id=self.request.user.id)

