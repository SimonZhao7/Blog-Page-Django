from rest_framework.serializers import ValidationError
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from account.models import CustomUser, UserFollowing, UserFriend
from chat.models import Chat, Messages
from notifications.models import Notification
from posts.models import Post, Comment
from django.core.files.storage import FileSystemStorage
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
import os


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
    
class BaseSettingSerializer(serializers.ModelSerializer):
    def validate(self, data):
        user = CustomUser.objects.get(id=self.context['id'])
        if not authenticate(username=user.username, password=data['password']):
            raise ValidationError('Incorrect Password')
        return data
    
    def save_instance(self, instance):
        instance.save()
        return instance
    
class ChangeUsernameSerializer(BaseSettingSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
        
    def validate(self, data):
        username = data['username']
        if len(username) < 6:
            raise ValidationError('Username is under 6 characters long')
        
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError('Username already exists')
        return super().validate(data)
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username')
        return super().save_instance(instance)
    
class ChangeEmailSerializer(BaseSettingSerializer):
    email = serializers.CharField()
    class Meta:
        model = CustomUser
        fields = ['email', 'password']
        
    def validate(self, data):
        email = data['email']
        validate_email(email)
        
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Email already exists')
        return super().validate(data)
        
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email')
        return super().save_instance(instance)
    
class ChangePasswordSerializer(BaseSettingSerializer):
    new_password = serializers.CharField(max_length=128, write_only=True)
    confirm_password = serializers.CharField(max_length=128, write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['password', 'new_password', 'confirm_password']
        
    def validate(self, data):
        pwd = data['new_password']
        validate_password(pwd)
        if pwd != data['confirm_password']:
            raise ValidationError("Passwords don't match")
        user_pwd = super().validate(data)['password']
        if pwd == user_pwd:
            raise ValidationError('Your new password can not be the same as your old one')
        return data
        
    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('new_password'))
        return super().save_instance(instance)
    
class ChangeProfilePictureSerializer(BaseSettingSerializer):
    class Meta:
        model = CustomUser
        fields = ['profile_picture', 'password']
        
    def update(self, instance, validated_data):
        photo = validated_data.get('profile_picture')
        fs = FileSystemStorage()
        saved_filepath = fs.save(os.path.join('profile_pictures', photo.name), photo)
        instance.profile_picture = saved_filepath
        return super().save_instance(instance)
                
class UserFollowingSerializer(ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = '__all__'
        
    def create(self, validated_data):
        user = validated_data.get('user')
        following = validated_data.get('following')
        if UserFollowing.objects.filter(user=following, following=user).exists():
            UserFriend.objects.create(user=user, friend=following)
            UserFriend.objects.create(user=following, friend=user)
        return super().create(validated_data)
        
class UserFriendSerializer(ModelSerializer):
    class Meta:
        model = UserFriend
        fields = '__all__'
        
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