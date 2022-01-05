from rest_framework.response import Response
from account.models import CustomUser, UserFollowing, UserFriend
from chat.models import Chat, Messages
from notifications.models import Notification
from posts.models import Post, Comment
from .serializers import CustomUserSerializer, MessagesSerializer, NotificationSerializer, UserFollowingSerializer, UserFriendSerializer, \
    ChatSerializer, PostSerializer, CommentSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin

# Create your views here.
class SharedView(GenericAPIView, ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin):
    lookup_field = 'id'
    
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
    
class UserFollowingAPIView(SharedView):
    serailizer_class = UserFollowingSerializer
    queryset = UserFollowing.objects.all()
    
class UserFriendAPIView(SharedView):
    serializer_class = UserFriendSerializer
    queryset = UserFriend.objects.all()
    
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
    queryset = Post.objects.all()
    
class CommentAPIView(SharedView):
    serializers = CommentSerializer
    queryset = Comment.objects.all()