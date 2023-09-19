from django.contrib import admin
from .models import Account, Follow
from .forms import AccountAdminForm


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'date_of_birth', 'gender', 'bio', 'phone_number', 'location', 'created_date']
    form = AccountAdminForm


admin.site.register(Follow)

