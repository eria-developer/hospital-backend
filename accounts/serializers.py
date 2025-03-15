# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User = get_user_model()  # Use default User model or custom model if defined


# Serializer for user registration
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.
    Handles user creation with password hashing.
    """
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}  # Password won't be returned in responses

    def create(self, validated_data):
        """
        Create a new user with hashed password using create_user.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


# Serializer for user login
class LoginSerializer(serializers.Serializer):
    """
    Serializer for validating login credentials.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)  # Password is write-only