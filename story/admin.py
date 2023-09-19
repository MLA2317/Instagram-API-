from django.contrib import admin
from .models import Story, StoryMarkFollower, Archive


admin.site.register(StoryMarkFollower)


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'content', 'caption', 'posted']


@admin.register(Archive)
class Archive(admin.ModelAdmin):
    list_display = ['id', 'story', 'archived_at']