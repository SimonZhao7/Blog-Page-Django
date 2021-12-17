from django.forms import ModelForm
from .models import Post
from django.utils import timezone


class CreatePostForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = Post
        fields = ['image', 'caption']
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        instance.date_time_posted = timezone.now()
        instance.likes = 0
        
        if commit:
            instance.save()
        return instance
        
        