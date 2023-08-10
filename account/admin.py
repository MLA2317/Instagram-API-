from django.contrib import admin
from .models import Account, Follower, Following, Location


admin.site.register(Account)
admin.site.register(Follower)
admin.site.register(Following)
admin.site.register(Location)


