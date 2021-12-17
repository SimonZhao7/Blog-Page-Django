from django.db import models
from account.models import CustomUser

# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField() # see if you can put restrictions here
    caption = models.TextField(blank=True)
    users_liked = models.ManyToManyField(CustomUser, related_name='users_liked')
    likes = models.IntegerField()
    date_time_posted = models.DateTimeField()
    
    def get_slug(self):
        return self.pk + 816020927
    
    @staticmethod
    def get_id(id):
        return int(id) - 816020927