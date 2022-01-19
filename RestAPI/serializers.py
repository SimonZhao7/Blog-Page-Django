from rest_framework.serializers import ValidationError
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from account.models import CustomUser, UserFollowing, UserFriend
from chat.models import Chat, Messages
from notifications.models import Notification
from posts.models import Post, Comment
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.Serializer): 
    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128)
    password2 = serializers.CharField(max_length=128, write_only=True)
    profile_picture = serializers.ImageField(default='/media/profile_pictures/no-profile.png')
    
    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise ValidationError('Email already exists')
        return value
    
    def validate_username(self, value):
        if len(value) < 6:
            raise ValidationError('Username is under 6 characters long')
        
        if CustomUser.objects.filter(username=value).exists():
            raise ValidationError('Username already exists')
        return value
        
    def validate_password(self, value):
        validate_password(value)
        return value
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise ValidationError('The passwords don\'t match')
        return data
        
    def create(self, validated_data):
        email = validated_data.get('email')
        username = validated_data.get('username')
        password = validated_data.get('password')
        profile_picture = validated_data.get('profile_picture')
        
        instance = CustomUser(email=email, username=username, profile_picture=profile_picture)
        instance.set_password(password)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.set_password(validated_data.get('password', instance.password))
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        return instance
        
        
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