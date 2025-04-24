from rest_framework import serializers
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    """
    Serializer for the Patient model.

    Serializes all fields of the Patient model for use in API requests and responses.

    Fields:
        - id (int): The unique identifier of the patient (read-only).
        - first_name (str): The patient's first name (required, max 100 characters).
        - last_name (str): The patient's last name (required, max 100 characters).
        - date_of_birth (date): The patient's date of birth in YYYY-MM-DD format (required).
        - gender (str): The patient's gender ('M', 'F', or 'O') (required).
        - medical_record_number (str): The unique medical record number (required, max 50 characters, unique).
        - phone (str): The patient's phone number (required, max 15 characters, must match phone format).
        - email (str): The patient's email address (optional, valid email format).
        - address (str): The patient's address (optional, can be blank).
        - emergency_contact_phone (str): The phone number of the emergency contact (optional, max 15 characters, must match phone format).
        - is_active (bool): Whether the patient is active (required, default true).
        - created_at (datetime): The creation timestamp of the patient record (read-only).
        - updated_at (datetime): The last update timestamp of the patient record (read-only).

    Usage:
        Used to validate and serialize patient data for creating, updating, or retrieving patients.
    """
    class Meta:
        model = Patient
        fields = '__all__'

    def validate_date_of_birth(self, value):
        """
        Validate that the date of birth is not in the future.

        Parameters:
            value (date): The date of birth to validate.

        Returns:
            date: The validated date of birth.

        Raises:
            ValidationError: If the date of birth is in the future.
        """
        from datetime import date
        if value > date.today():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return value

    def validate_medical_record_number(self, value):
        """
        Validate that the medical record number is not already in use (for create operations).

        Parameters:
            value (str): The medical record number to validate.

        Returns:
            str: The validated medical record number.

        Raises:
            ValidationError: If the medical record number is already in use.
        """
        if self.instance is None and Patient.objects.filter(medical_record_number=value).exists():
            raise serializers.ValidationError("A patient with this medical record number already exists.")
        return value