from rest_framework.serializers import ValidationError
from rest_framework.serializers import ModelSerializer
from account.models import CustomUser, UserFollowing, UserFriend
from chat.models import Chat, Messages
from notifications.models import Notification
from posts.models import Post, Comment
from django.contrib.auth.password_validation import validate_password


class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        
    def validate_username(self, value):
        if len(value) < 6:
            raise ValidationError('Username is under 6 characters long')
        return value
    
    def validate_password(self, value):
        validate_password(value)
        return value
    
    def save(self, **kwargs):
        instance = super().save(**kwargs)
        instance.set_password(self.validated_data['password'])
        instance.save()
        
class UserFollowingSerializer(ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = '__all__'
        
class UserFriendSerializer(ModelSerializer):
    class Meta:
        model = UserFriend
        fields = '__all__'
        
class ChatSerializer(ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'
        
class MessagesSerializer(ModelSerializer):
    class Meta:
        model = Messages
        fields = '__all__'
        
class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        
class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        
class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'