from django.db import models
from django.contrib.auth.models import AbstractUser
import json

# Create your models here.


class CustomUser(AbstractUser):
    profile_picture = models.TextField()

    # Add in Follower app
    # followers = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # following = models.TextField(default=json.dumps([]))
    # friends = models.TextField(default=json.dumps([]))
