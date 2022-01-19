from django.urls import path
from rest_framework.authtoken import views as auth_views
from . import views

app_name = 'RestAPI'

urlpatterns = [
    path('CustomUserAPI/', views.CustomUserAPIView.as_view(), name='CustomUserAPI'),
    path('CustomUserAPI/<int:id>/', views.CustomUserAPIView.as_view(), name='CustomUserAPI'),
    path('CustomUserAPI/token=<str:token>/', views.CustomUserAPIView.as_view(), name='CustomUserAPI'),
    path('CustomUserAPI/username=<str:username>/', views.CustomUserAPIView.as_view(), name='CustomUserAPI'),
    path('UserFollowingAPI/', views.UserFollowingAPIView.as_view(), name='UserFollowingAPI'),
    path('UserFollowingAPI/<int:id>/', views.UserFollowingAPIView.as_view(), name='UserFollowingAPI'),
    path('UserFriendAPI/', views.UserFriendAPIView.as_view(), name='UserFriendAPI'),
    path('UserFriendAPI/<int:id>/', views.UserFriendAPIView.as_view(), name='UserFriendAPI'),
    path('ChatAPI/', views.ChatAPIView.as_view(), name='ChatAPI'),
    path('ChatAPI/<int:id>/', views.ChatAPIView.as_view(), name='ChatAPI'),
    path('MessageAPI/', views.MessagesAPIView.as_view(), name='MessageAPI'),
    path('MessageAPI/<int:id>/', views.MessagesAPIView.as_view(), name='MessageAPI'),
    path('NotificationAPI/', views.NotificationAPIView.as_view(), name='NotificationAPI'),
    path('NotificationAPI/<int:id>/', views.NotificationAPIView.as_view(), name='NotificationAPI'),  
    path('PostAPI/', views.PostAPIView.as_view(), name='PostAPI'),
    path('PostAPI/<int:id>/', views.PostAPIView.as_view(), name='PostAPI'),
    path('CommentAPI/', views.CommentAPIView.as_view(), name='CommentAPI'),
    path('CommentAPI/<int:id>/', views.CommentAPIView.as_view(), name='CommentAPI'),
    path('login/', auth_views.obtain_auth_token, name='login'),
    path('register/', views.RegisterAPIView.as_view(), name='register'),
]