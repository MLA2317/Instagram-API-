# # from celery import shared_task
# # from django.utils import timezone
# # from .models import Story, Archive
# #
# #
# # @shared_task
# # def archive_expired_stories():
# #     expired_stories = Story.objects.filter(expires_at__lte=timezone.now(), is_archived=False)
# #
# #     for story in expired_stories:
# #         Archive.objects.create(
# #             story=story,
# #             user_id=story.user,
# #             content=story.content
# #         )
# #         story.is_archived = True
# #         story.save()
#
#
# from datetime import datetime, timedelta
# from celery import shared_task
# from .models import Story, Archive
# from django.db import transaction
#
#
# @shared_task
# def archive_expired_stories():
#     with transaction.atomic():
#         # 24 soatdan keyin arxivlanmagan hikoyalarni toping
#         expiry_time = datetime.now() - timedelta(minutes=5)
#         print('expire', expiry_time)
#
#         stories_to_archive = Story.objects.filter(posted__lte=expiry_time, is_archived=False)
#
#         for story in stories_to_archive:
#             # Hikoyani arxivlang
#             Archive.objects.create(story_id=story)
#             story.is_archived = True
#             story.delete()
#             print(f"Archived story with ID: {story.id}")
#
