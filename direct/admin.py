from django.contrib import admin
from .models import DirectMessage

@admin.register(DirectMessage)
class DirectMessageAdmin(admin.ModelAdmin):
    list_editable = ['is_read']
    list_display = ['id', 'sender', 'receiver', 'file', 'is_read', 'created_date']