from rest_framework.response import Response
from account.models import CustomUser, UserFollowing, UserFriend
from chat.models import Chat, Messages
from notifications.models import Notification
from posts.models import Post, Comment
from .serializers import ChangeEmailSerializer, ChangePasswordSerializer, ChangeProfilePictureSerializer, CustomUserSerializer, RegisterSerializer, MessagesSerializer, NotificationSerializer, UserFollowingSerializer, UserFriendSerializer, \
    ChatSerializer, PostSerializer, CommentSerializer, ChangeUsernameSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .permissions import AllowPOSTOnly

# Create your views here.
class SharedView(GenericAPIView, ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin):
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id=None):
        if id:
            return self.retrieve(request, id=id)
        else:
            return self.list(request)
        
    def post(self, request, id=None):
        if id:
            return Response({"error": "Cannot specify an id"})
        else:
            return self.create(request)
    
    def put(self, request, id=None):
        if id:
            return self.update(request, id)
        else:
            return Response({"error": "Need to specify an id."})
        
    def delete(self, request, id=None):
        if id:
            return self.destroy(request, id)
        else:
            return Response({"error": "Need to specify an id."})    
        

class CustomUserAPIView(SharedView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    
    def get(self, request, id=None, token=None, username=None, type=None, search_value=None):
        if type:
            return Response({'error': "Type argument not allowed"})
        
        if id:
            try:
                user = CustomUser.objects.get(id=id)
            except: 
                return Response({'error': "Can't find use with provided id"})
            return Response(self.serializer_class(user).data)
        elif token:
            try:
                user = CustomUser.objects.get(auth_token__key=token)
            except:
                return Response({'error': "Can't find user with provided token"})
            return Response(self.serializer_class(user).data)
        elif username:
            try:
                user = CustomUser.objects.get(username=username)
            except:
                return Response({'error': "Can't find user with provided username"})
            return Response(self.serializer_class(user).data)
        elif search_value:
            try:
                users = CustomUser.objects.filter(username__icontains=search_value)
                return Response(self.serializer_class(users, many=True).data)
            except:
                return Response({'error': 'There was a problem fetching search results'})
        else:
            return self.list(request)
        
    def post(self, request, id=None, type=None, username=None, token=None, search_value=None):
        return Response({"error": "This method is not allowed for CustomUser. Use RegisterAPIView"})
    
    def put(self, request, id=None, type=None, username=None, token=None, search_value=None):
        if username or token:
            return Response({'error': "Argument not allowed"})
        
        if id:
            if type == 'change_username':
                self.serializer_class = ChangeUsernameSerializer
            elif type == 'change_password':
                self.serializer_class = ChangePasswordSerializer
            elif type == 'change_email':
                self.serializer_class = ChangeEmailSerializer
            elif type == 'change_profile_picture':
                self.serializer_class = ChangeProfilePictureSerializer
            else:
                return Response({"error": "Invalid type"})
            
            context = {'id': id}
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=False, context=context)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"error": "Need to specify an id."})
    
    
class RegisterAPIView(SharedView):
    permission_classes = [AllowPOSTOnly]
    serializer_class = RegisterSerializer
    queryset = CustomUser.objects.all()
    
class UserFollowingAPIView(SharedView):
    serializer_class = UserFollowingSerializer
    queryset = UserFollowing.objects.all()
    
    def get(self, request, id=None, user_id=None, following_id=None):
        if id:
            return self.retrieve(request, id=id)
        elif user_id:
            user_following = UserFollowing.objects.filter(user=user_id)
            return Response(self.serializer_class(user_following, many=True).data)
        elif following_id:
            user_following = UserFollowing.objects.filter(following=following_id)
            return Response(self.serializer_class(user_following, many=True).data)
        else:
            return self.list(request)
        
    def perform_destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user
        following = instance.following
        friends = UserFriend.objects.filter(Q(user=user, friend=following) | Q(user=following, friend=user))
        for friend in friends:
            friend.delete()
        return super().perform_destroy(request, *args, **kwargs)
        
    
class UserFriendAPIView(SharedView):
    serializer_class = UserFriendSerializer
    queryset = UserFriend.objects.all()
    
    def get(self, request, id=None, user_id=None):
        if id:
            return self.retrieve(request, id=id)
        elif user_id:
            user_following = UserFollowing.objects.filter(user=user_id)
            if not user_following.exists():
                return Response("Can't find use with provided user_id")
            return Response(self.serializer_class(user_following, many=True).data)
        else:
            return self.list(request)
        
class ChatAPIView(SharedView):
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()
    
class MessagesAPIView(SharedView):
    serializer_class = MessagesSerializer
    queryset = Messages.objects.all()
    
class NotificationAPIView(SharedView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    
class PostAPIView(SharedView):
    serializer_class = PostSerializer
    queryset = Post.objects.order_by('date_time_posted').reverse()
    
class CommentAPIView(SharedView):
    serializers = CommentSerializer
    queryset = Comment.objects.all()