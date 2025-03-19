from django.urls import path
from .views import RegisterView, LoginView, UserProfileView, ChangePasswordView, UpdateUserRoleView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # Registration endpoint
    path('login/', LoginView.as_view(), name='login'),     # Login endpoint
    path('profiles/<int:user_id>/', UserProfileView.as_view(), name='user-profile'),
    path('profile/<int:user_id>/', UserProfileView.as_view(), name='user-profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('update-role/<int:user_id>/', UpdateUserRoleView.as_view(), name='update-role'),
]