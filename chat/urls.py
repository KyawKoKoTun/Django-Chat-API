
from django.urls import path
from .views import MessageCreateView, MessageListView

urlpatterns = [
    path('messages/', MessageCreateView.as_view(), name='create-message'),
    path('messages/list/', MessageListView.as_view(), name='list-messages'),
]
