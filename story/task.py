# from celery import shared_task
# from django.utils import timezone
# from .models import Story, Archive
#
#
# @shared_task
# def archive_expired_stories():
#     expired_stories = Story.objects.filter(expires_at__lte=timezone.now(), is_archived=False)
#
#     for story in expired_stories:
#         Archive.objects.create(
#             story=story,
#             user_id=story.user,
#             content=story.content
#         )
#         story.is_archived = True
#         story.save()
