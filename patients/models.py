from django.db import models
from django.core.validators import RegexValidator


class Patients(models.Model):
    """
    Model representing a patient in the hospital management system.

    Tracks essential information about patients including:
    - Personal details (name, date of birth, gender, etc.)
    - Contact information (phone, email, address)
    - Medical record identification
    """
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    medical_record_number = models.CharField(
        max_length=50,
        unique=True,
        help_text="Unique medical record number for the patient"
    )
    phone = models.CharField(
        max_length=15
    )
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    emergency_contact_phone = models.CharField(
        max_length=15,
        blank=True,
    )
    is_active = models.BooleanField(default=True, help_text="Indicates if the patient is currently active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        """
        Return a string representation of the patient.
        """
        return f"{self.first_name} {self.last_name} ({self.medical_record_number})"