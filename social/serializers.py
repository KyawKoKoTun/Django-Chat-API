from rest_framework import serializers
from .models import Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'user', 'contact', 'added_at']
        read_only_fields = ['id', 'user', 'added_at']
