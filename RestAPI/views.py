from rest_framework.response import Response
from account.models import CustomUser, UserFollowing, UserFriend
from chat.models import Chat, Messages
from notifications.models import Notification
from posts.models import Post, Comment
from .serializers import CustomUserSerializer, RegisterSerializer, MessagesSerializer, NotificationSerializer, UserFollowingSerializer, UserFriendSerializer, \
    ChatSerializer, PostSerializer, CommentSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
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
    
    def get(self, request, id=None, token=None, username=None):
        if id:
            try:
                user = CustomUser.objects.get(id=id)
            except: 
                return Response("Can't find use with provided id")
            return Response(self.serializer_class(user).data)
        elif token:
            try:
                user = CustomUser.objects.get(auth_token__key=token)
            except:
                return Response("Can't find user with provided token")
            return Response(self.serializer_class(user).data)
        elif username:
            try:
                user = CustomUser.objects.get(username=username)
            except:
                return Response("Can't find user with provided username")
            return Response(self.serializer_class(user).data)
        else:
            return self.list(request)
        
    def post(self, request, id=None):
        return Response({"error": "This method is not allowed for CustomUser. Use RegisterAPIView"})
    
    
class RegisterAPIView(SharedView):
    permission_classes = [AllowPOSTOnly]
    serializer_class = RegisterSerializer
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