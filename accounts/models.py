from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.
    Provides additional fields for hospital staff role management and contact information.
    """
    USER_ROLES = (
        ('admin', 'Administrator'),
        ('doctor', 'Doctor'),
        ('nurse', 'Nurse'),
        ('accountant', 'Accountant'),
        ('receptionist', 'Receptionist'),
        ('lab_technician', 'Laboratory Technician'),
        ('pharmacist', 'Pharmacist'),
        ('staff', 'General Staff'),
    )
    role = models.CharField(max_length=20, choices=USER_ROLES, default='staff')
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    

# Linking profiles to users
class PatientProfile(models.Model):
    """
    Profile model for patients.
    Stores patient-specific information.
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    address = models.TextField()
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username} (Patient)"
    

class DoctorProfile(models.Model):
    """
    Profile model for doctors.
    Stores doctor-specific information.
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=50, unique=True)
    years_of_experience = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username} (Doctor)"