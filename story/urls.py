from django.urls import path, include
from .views import StoryListCreate, StoryDestroy, ArchiveList

urlpatterns = [
    path('story/list-create/', StoryListCreate.as_view()),
    path('story/<int:pk>/delete/', StoryDestroy.as_view()),
    path('archive/list/', ArchiveList.as_view()),

    path('v1', include('story.v1.urls', namespace='story'))
]
