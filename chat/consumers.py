from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import Message


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        contact_hash = self.scope["url_route"]["kwargs"].get("contact_hash")

        if contact_hash:
            self.contact_hash = contact_hash
            async_to_sync(self.channel_layer.group_add)(
                self.contact_hash, self.channel_name
            )
            self.accept()
        else:
            self.close()

    def disconnect(self, close_code):
        if hasattr(self, "contact_hash"):
            async_to_sync(self.channel_layer.group_discard)(
                self.contact_hash, self.channel_name
            )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_text = text_data_json.get("message", "")

        if hasattr(self, "contact_hash"):
            user = self.scope["user"]
            recipient = self.get_recipient_from_contact_hash(self.contact_hash, user)

            if recipient:
                message = Message.objects.create(
                    user=user, to=recipient, text=message_text
                )

                async_to_sync(self.channel_layer.group_send)(
                    self.contact_hash,
                    {
                        "type": "chat_message",
                        "message": message_text,
                        "user": user.username,
                        "created_at": message.created_at.isoformat(),
                    },
                )

    def chat_message(self, event):
        self.send(
            text_data=json.dumps(
                {
                    "message": event["message"],
                    "user": event["user"],
                    "created_at": event["created_at"],
                }
            )
        )

    def get_recipient_from_contact_hash(self, contact_hash, user):
        from .models import Contact

        contact = Contact.objects.filter(unique_hash=contact_hash).first()
        if contact:
            if contact.user == user:
                return contact.contact
            elif contact.contact == user:
                return contact.user
        return None
