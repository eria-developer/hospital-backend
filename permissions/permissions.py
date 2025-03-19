# from rest_framework.permissions import BasePermission

# class IsAdminUser(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.role == "admin"
    

# class IsAdminOrOwner(BasePermission):
#     """
#     Permission to allow access to admins or the owner of the profile.
#     """
#     def has_permission(self, request, view):
#         # Check if the user is authenticated
#         if not request.user or not request.user.is_authenticated:
#             return False
#         # Allow access if the user is an admin
#         if request.user.role == 'admin':
#             return True
#         # For non-admins, allow access only if the user_id in the URL matches their own ID
#         user_id = view.kwargs.get('user_id')
#         try:
#             user_id = int(user_id)
#             return user_id == request.user.id
#         except (TypeError, ValueError):
#             return False









# permissions/permissions.py
from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """
    Permission class that only allows access to users with 'admin' role.
    Used for admin-specific operations like changing user roles.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"
    
class IsAdminOrOwner(BasePermission):
    """
    Permission to allow access to admins or the owner of the profile.
    Used for profile management where both admins and the user themselves
    should have access to the resource.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Allow access if the user is an admin
        if request.user.role == 'admin':
            return True
        
        # For non-admins, allow access only if the user_id in the URL matches their own ID
        user_id = view.kwargs.get('user_id')
        try:
            user_id = int(user_id)
            return user_id == request.user.id
        except (TypeError, ValueError):
            return False

class IsDoctorOrAdmin(BasePermission):
    """
    Permission class that allows access to users with 'doctor' or 'admin' roles.
    Useful for endpoints that should be accessed by medical professionals or administrators.
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                request.user.role in ["doctor", "admin"])

class IsAccountantOrAdmin(BasePermission):
    """
    Permission class that allows access to users with 'accountant' or 'admin' roles.
    Useful for financial and billing-related endpoints.
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                request.user.role in ["accountant", "admin"])

class IsStaffUser(BasePermission):
    """
    Permission class that allows access to any authenticated user with a staff role.
    This includes all roles except patients.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role != "patient"