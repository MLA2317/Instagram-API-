from datetime import timedelta
from django.utils import timezone
from .models import Story
from celery import shared_task


@shared_task
def delete_old_stories():
    time_threshold = timezone.now() - timedelta(minutes=2)
    old_stories = Story.objects.filter(posted__lte=time_threshold)
    old_stories.delete()
