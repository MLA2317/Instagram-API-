# # import os
# #
# # from celery import Celery
# # from django.conf import settings
# # from story.task import archive_expired_stories
# #
# #
# # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# #
# # app = Celery('config')
# # app.config_from_object('django.conf:settings', namespace='CELERY')
# # app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
# # app.register_task(archive_expired_stories)
# # print(app.tasks.keys())
#
# import os
# from celery import Celery
# from django.conf import settings
#
# # Set the default Django settings module.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
#
# app = Celery('config')
#
# # Use the Django settings for the Celery app.
# app.config_from_object('django.conf:settings', namespace='CELERY')
#
# # Load task modules from all registered Django app configs.
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
