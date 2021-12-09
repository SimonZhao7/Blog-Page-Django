from channels.routing import ProtocolTypeRouter, URLRouter
from chat.consumers import ChatConsumer
from django.urls import path


application = ProtocolTypeRouter({
    'websocket': URLRouter([
        path('ws/chat/', ChatConsumer.as_asgi()),
    ])
})