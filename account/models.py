from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    profile_picture = models.FileField()

    # Add:
    # friends = models.TextField(default=json.dumps([]))


class UserFollowing(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    following = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='following', null=True)

    def __str__(self):
        return self.user.username
