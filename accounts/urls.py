from django.urls import path
from .views import RegisterView, LoginView, UserProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # Registration endpoint
    path('login/', LoginView.as_view(), name='login'),     # Login endpoint
    path('profiles/<int:user_id>/', UserProfileView.as_view(), name='user-profile'),
]