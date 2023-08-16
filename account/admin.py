from django.contrib import admin
from .models import Account, Follow, Location


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'date_of_birth', 'gender', 'bio', 'phone_number', 'location', 'created_date']


admin.site.register(Follow)
admin.site.register(Location)
