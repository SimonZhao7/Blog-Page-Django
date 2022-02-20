from django.forms import ModelForm
from .models import Comment, Post
from django.utils import timezone
from django import forms


ASPECT_RATIO_CHOICES = (
    ('one-one', '1 : 1'),
    ('four-three', '4 : 3'),
    ('sixteen-nine', '16 : 9'),
    ('nine-sixteen', '9 : 16'),
)


class CreatePostForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = Post
        fields = ['aspect_ratio', 'image', 'caption']
        widgets = {
            'aspect_ratio': forms.Select(choices=ASPECT_RATIO_CHOICES, attrs={'class': 'custom-select'}),
            'caption': forms.Textarea(attrs={'class': 'form-control'})
        }
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        
        if commit:
            instance.save()
        return instance
    
    
class ReplyForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['message']    