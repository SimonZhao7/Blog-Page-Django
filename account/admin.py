from django.contrib import admin
from .models import CustomUser, UserFollowing, UserFriend

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(UserFollowing)
admin.site.register(UserFriend)