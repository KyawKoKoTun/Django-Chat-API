from django.urls import path
from chat import consumers

websocket_urlpatterns = [
    path('ws/chat/<str:contact_hash>/', consumers.ChatConsumer.as_asgi()),
]
