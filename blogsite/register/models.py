from django.db import models
from django.contrib.auth.models import User
import json

# Create your models here.


class Profile(User):
    profile_picture = models.TextField(default='/')
    followers = models.TextField(default=json.dumps([]))
    following = models.TextField(default=json.dumps([]))
    friends = models.TextField(default=json.dumps([]))
