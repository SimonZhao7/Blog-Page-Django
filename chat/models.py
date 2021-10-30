from django.db import models
from account.models import CustomUser

# Create your models here.


class Chat(models.Model):
    users = models.ManyToManyField(CustomUser)
    name = models.CharField(max_length=200)

    def get_slug(self):
        return self.pk + 344271648

    @staticmethod
    def get_id(slug):
        return int(slug) - 344271648

    def __str__(self):
        return self.name


class Messages(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    message = models.TextField()

    # might need a time created for ordering purposes
