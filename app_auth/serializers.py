from .models import User
from rest_framework import serializers
import datetime


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    # date_of_birth = serializers.DateField(required=False)

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            # date_of_birth=validated_data['date_of_birth'],
        )
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['photo', 'date_of_birth', 'username']
        extra_kwargs = {
            'photo': {'required': False},
            'date_of_birth': {'required': False},
            'username': {'required': False},
        }

    def validate_username(self, value):
        return value
