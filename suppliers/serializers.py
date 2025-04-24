from rest_framework import serializers
from .models import Supplier


class SupplierSerializer(serializers.ModelSerializer):
    """
    Serializer for the Supplier model.

    Serializes all fields of the Supplier model for use in API requests and responses.

    Fields:
        - id (int): The unique identifier of the supplier (read-only).
        - name (str): The name of the supplier (required, max 100 characters).
        - registration_number (str): A unique registration number for the supplier (required, max 30 characters).
        - email (str): The email address of the supplier (required, valid email format).
        - phone (str): The primary phone number of the supplier (required, max 15 characters).
        - alternative_phone (str): An alternative phone number (optional, max 15 characters, nullable).
        - address (str): The address of the supplier (optional, can be blank).
        - description (str): A description of the supplier (optional, nullable).

    Usage:
        Used to validate and serialize supplier data for creating, updating, or retrieving suppliers.
    """
    class Meta:
        model = Supplier
        fields = '__all__'  # Include all fields from the Supplier model