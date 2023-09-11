from django.contrib import admin
from .models import Story, StoryMarkFollower, Archive

admin.site.register(Story)
admin.site.register(StoryMarkFollower)
admin.site.register(Archive)

