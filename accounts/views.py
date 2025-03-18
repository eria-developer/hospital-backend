# accounts/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from .serializers import UserSerializer, LoginSerializer, UserProfileSerializer, PatientProfileSerializer, DoctorProfileSerializer
from permissions.permissions import IsAdminUser, IsAdminOrOwner
from .models import CustomUser, PatientProfile, DoctorProfile

# Registration view
class RegisterView(APIView):
    """
    API endpoint for registering a new user.
    Accepts POST requests with username, email, and password.
    Returns user data and an authentication token.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Create the user
            token, _ = Token.objects.get_or_create(user=user)  # Generate or retrieve token
            return Response({
                'user': UserSerializer(user).data,  # User details (no password)
                'token': token.key  # Authentication token
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login view
class LoginView(APIView):
    """
    API endpoint for logging in a user.
    Accepts POST requests with username and password.
    Returns an authentication token if credentials are valid.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)  # Verify credentials
            if user:
                token, _ = Token.objects.get_or_create(user=user)  # Get or create token
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserProfileView(APIView):
    permission_classes = [IsAdminOrOwner]

    def get(self, request, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
            serializer = UserProfileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
            role = user.role
            profile_data = request.data.get('profile', {})

            if role == 'patient':
                profile, created = PatientProfile.objects.get_or_create(user=user)
                serializer = PatientProfileSerializer(profile, data=profile_data, partial=True)
            elif role == 'doctor':
                profile, created = DoctorProfile.objects.get_or_create(user=user)
                serializer = DoctorProfileSerializer(profile, data=profile_data, partial=True)
            else:
                return Response({"error": "Invalid user role"}, status=status.HTTP_400_BAD_REQUEST)

            if serializer.is_valid():
                serializer.save()
                return Response(UserProfileSerializer(user).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)