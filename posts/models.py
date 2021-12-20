from django.db import models
from account.models import CustomUser

# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    aspect_ratio = models.CharField(max_length=20, null=True)
    image = models.ImageField()
    caption = models.TextField(blank=True)
    users_liked = models.ManyToManyField(CustomUser, related_name='users_liked')
    likes = models.IntegerField()
    date_time_posted = models.DateTimeField()
    
    def get_slug(self):
        return self.pk + 816020927
    
    @staticmethod
    def get_id(id):
        return int(id) - 816020927
    
    def get_ratio_class(self):
        return self.aspect_ratio