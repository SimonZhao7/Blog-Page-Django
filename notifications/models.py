from re import template
from django.db import models
from account.models import CustomUser

# Create your models here.


class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    detail = models.CharField(max_length=100)
    link = models.URLField(max_length=200)
    has_seen = models.BooleanField(default=False)
    date_created = models.DateTimeField()
    
    def get_slug(self):
        return self.pk + 618464911
    
    @staticmethod
    def get_id(slug):
        return int(slug) - 618464911
    
    def __str__(self):
        return self.user