from channels.consumer import SyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
from account.models import CustomUser
from .models import Messages, Chat
import re, json


class ChatConsumer(SyncConsumer):
    def websocket_connect(self, event):
        self.room_name = 'chat'
        self.send({
            'type': 'websocket.accept'
        })
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)

    def websocket_receive(self, event):
        print("Message Received")
        print(event)
        
        # Create new instance here
        sent_data = json.loads(event['text'])
        
        slug = re.search(r'[0-9]{7}[0-9]*', sent_data['url']).group()
        current_chat = Chat.objects.get(id=Chat.get_id(slug))
        sender = CustomUser.objects.get(username=sent_data['sender'])
        msg_content = sent_data['message']
        
        new_message = Messages(chat=current_chat, message=msg_content, sender=sender)
        new_message.save()
        
        async_to_sync(self.channel_layer.group_send)(
            self.room_name,
            {
                'type': 'websocket.message',
                'text': event.get('text')
            }
        )
        
    def websocket_message(self, event):
        self.send({
            'type': 'websocket.send',
            'text': event.get('text')
        })

    def websocket_disconnect(self, event):
        print("Connect event closed")
        print(event)
        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)
        raise StopConsumer()
