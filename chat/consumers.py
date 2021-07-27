from channels.consumer import SyncConsumer


class ChatConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print("Connect event called")

        self.send({
            'type': 'websocket.accept'
        })

    def websocket_receive(self, event):
        print("Message Received")
        print(event)

        self.send({
            'type': 'websocket.send',
            'text': event.get('text')
        })

    def websocket_disconnect(self, event):
        print("Connect event closed")
        print(event)
