from django.db import models
from accounts.models import DoctorProfile

class Specialty(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    profile = models.OneToOneField(DoctorProfile, on_delete=models.CASCADE)
    specialty = models.ForeignKey(Specialty, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Dr. {self.profile.user.first_name} {self.profile.user.last_name}"