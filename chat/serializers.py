from rest_framework import serializers
from .models import Message, FileAttachment


class FileAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileAttachment
        fields = ["id", "file", "uploaded_at"]
        read_only_fields = ["id", "uploaded_at"]


class MessageSerializer(serializers.ModelSerializer):
    attachments = FileAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Message
        fields = ["id", "user", "text", "attachments", "created_at"]
        read_only_fields = ["id", "user", "created_at"]
