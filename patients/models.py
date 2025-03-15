from django.db import models
from accounts.models import PatientProfile

class Patient(models.Model):
    profile = models.OneToOneField(PatientProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.profile.user.first_name} {self.profile.user.last_name}"