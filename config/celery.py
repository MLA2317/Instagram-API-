# import os
# from celery import Celery
# from django.conf import settings
# from celery.schedules import crontab
#
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
#
#
# app = Celery('story')
#
#
# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
#
# app.conf.beat_schedule = {
#     'delete_old_stories_everyday': {
#         'task': 'story.task.delete_old_stories',
#         'schedule': crontab(minute=2, hour=0),  # Run daily at midnight
#     },
# }
#
