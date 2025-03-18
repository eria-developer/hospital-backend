from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"
    

class IsAdminOrOwner(BasePermission):
    """
    Permission to allow access to admins or the owner of the profile.
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