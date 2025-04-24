
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from .models import DoctorProfile, PatientProfile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user creation and general user information.
    Handles password hashing when creating users.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role', 'phone_number', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},  # Password won't be returned in responses
            'id': {'read_only': True}  # ID is read-only
        }

    def create(self, validated_data):
        """
        Create a new user with hashed password using create_user.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            role=validated_data.get('role', 'staff'),
            phone_number=validated_data.get('phone_number', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user
    
    def update(self, instance, validated_data):
        """
        Update user details while handling password separately to ensure it's hashed.
        """
        password = validated_data.pop('password', None)
        
        # Update all other fields
        for key, value in validated_data.items():
            setattr(instance, key, value)
        
        # Handle password update if provided
        if password:
            instance.set_password(password)
            
        instance.save()
        return instance

class LoginSerializer(serializers.Serializer):
    """
    Serializer for validating login credentials.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)  # Password is write-only

class PatientProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for patient-specific profile information.
    """
    class Meta:
        model = PatientProfile
        fields = ['date_of_birth', 'gender', 'address', 'emergency_contact_name', 'emergency_contact_phone']

class DoctorProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for doctor-specific profile information.
    """
    class Meta:
        model = DoctorProfile
        fields = ['license_number', 'years_of_experience']

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Combined serializer for user information and their role-specific profile.
    """
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'phone_number', 'first_name', 'last_name', 'profile']

    def get_profile(self, obj):
        """
        Get the role-specific profile information for the user.
        """
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

class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for changing a user's password.
    Validates that the new password and confirmation match.
    """
    current_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, data):
        """
        Validate that the new password and confirmation match.
        """
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("New passwords do not match.")
        return data

class UserRoleUpdateSerializer(serializers.Serializer):
    """
    Serializer for updating a user's role.
    Validates that the role is one of the allowed choices.
    """
    role = serializers.ChoiceField(choices=User.USER_ROLES)