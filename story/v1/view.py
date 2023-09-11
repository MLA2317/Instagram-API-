from django.shortcuts import render, redirect
from .forms import StoryForm
from ..task import archive_expired_stories
from ..models import Story, Archive
from django.utils import timezone


def upload_story(request):
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user
            story.expires_at = timezone.now() + timezone.timedelta(days=1)
            story.save()

            archive_expired_stories.delay(story.id)

            return redirect('view_stories')
    else:
        form = StoryForm()

    return render(request, 'story/story.html', {'form': form})


def archive_stories(request):
    archived_stories = Archive.objects.filter(user=request.user)
    return render(request, 'story/archive.html', {'archive_story': archived_stories})
