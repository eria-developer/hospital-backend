from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from .serializers import (
    UserSerializer, LoginSerializer, UserProfileSerializer, 
    PasswordChangeSerializer, UserRoleUpdateSerializer, 
    DoctorProfileSerializer, PatientProfileSerializer
)
from permissions.permissions import IsAdminUser, IsAdminOrOwner
from .models import CustomUser, DoctorProfile, PatientProfile

class RegisterView(APIView):
    """
    API endpoint for registering a new user.
    Accepts POST requests with username, email, password, and optional role.
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

class LoginView(APIView):
    """
    API endpoint for logging in a user.
    Accepts POST requests with username and password.
    Returns an authentication token and user details if credentials are valid.
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
                # Return user details along with token
                user_data = UserProfileSerializer(user).data
                return Response({
                    'token': token.key,
                    'user': user_data
                }, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """
    API endpoint for retrieving and updating user profile information.
    Only admins or the profile owner can access this endpoint.
    """
    permission_classes = [IsAdminOrOwner]

    def get(self, request, user_id):
        """
        Get a user's profile information.
        """
        try:
            user = CustomUser.objects.get(id=user_id)
            self.check_object_permissions(request, user)  # Check if user has permission
            serializer = UserProfileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, user_id):
        """
        Update a user's profile information.
        """
        try:
            user = CustomUser.objects.get(id=user_id)
            self.check_object_permissions(request, user)  # Check if user has permission
            
            # Update basic user information
            user_data = request.data.get('user', {})
            user_serializer = UserSerializer(user, data=user_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
            else:
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            # Update profile-specific information
            profile_data = request.data.get('profile', {})
            if profile_data:
                if user.role == 'patient':
                    profile, created = PatientProfile.objects.get_or_create(user=user)
                    profile_serializer = PatientProfileSerializer(profile, data=profile_data, partial=True)
                elif user.role == 'doctor':
                    profile, created = DoctorProfile.objects.get_or_create(user=user)
                    profile_serializer = DoctorProfileSerializer(profile, data=profile_data, partial=True)
                else:
                    # For other roles without specific profiles
                    return Response(UserProfileSerializer(user).data, status=status.HTTP_200_OK)
                
                if profile_serializer.is_valid():
                    profile_serializer.save()
                    return Response(UserProfileSerializer(user).data, status=status.HTTP_200_OK)
                return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(UserProfileSerializer(user).data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class ChangePasswordView(APIView):
    """
    API endpoint for changing a user's password.
    Requires authentication. Users can only change their own passwords.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Change the authenticated user's password.
        Requires current_password and new_password in request data.
        """
        user = request.user
        serializer = PasswordChangeSerializer(data=request.data)
        
        if serializer.is_valid():
            # Check if the current password is correct
            if not user.check_password(serializer.validated_data['current_password']):
                return Response({"error": "Current password is incorrect"}, 
                                status=status.HTTP_400_BAD_REQUEST)
            
            # Set the new password
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            # Update token to force re-login with new password
            Token.objects.filter(user=user).delete()
            token, _ = Token.objects.get_or_create(user=user)
            
            return Response({
                "message": "Password changed successfully",
                "new_token": token.key
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserRoleView(APIView):
    """
    API endpoint for updating a user's role.
    Only administrators can access this endpoint.
    """
    permission_classes = [IsAdminUser]
    
    def put(self, request, user_id):
        """
        Update a user's role.
        Requires role in request data.
        """
        try:
            user = CustomUser.objects.get(id=user_id)
            serializer = UserRoleUpdateSerializer(data=request.data)
            
            if serializer.is_valid():
                # Update the user's role
                user.role = serializer.validated_data['role']
                user.save()
                
                return Response({
                    "message": "User role updated successfully",
                    "user": UserProfileSerializer(user).data
                }, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
