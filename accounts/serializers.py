# accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from accounts.models import PatientProfile, DoctorProfile

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


# Serializer for PatientProfile
class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = ['date_of_birth', 'gender', 'address', 'emergency_contact_name', 'emergency_contact_phone']

# Serializer for DoctorProfile
class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = ['license_number', 'years_of_experience']


# Combined serializer for CustomUser and their profile
class UserProfileSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'profile']

    def get_profile(self, obj):
        if obj.role == 'patient':
            try:
                return PatientProfileSerializer(obj.patientprofile).data
            except PatientProfile.DoesNotExist:
                return None
        elif obj.role == 'doctor':
            try:
                return DoctorProfileSerializer(obj.doctorprofile).data
            except DoctorProfile.DoesNotExist:
                return None
        return None