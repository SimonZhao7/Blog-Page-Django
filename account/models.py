from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField()
    profile_picture = models.ImageField()


class UserFollowing(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    following = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='following', null=True)

    def __str__(self):
        return self.user.username


class UserFriend(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    friend = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='friend')

    def __str__(self):
        return self.user.username
