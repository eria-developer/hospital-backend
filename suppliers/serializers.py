from rest_framework import serializers
from .models import Supplier

class SupplierSerializer(serializers.ModelSerializer):
    """
    Serializer for the Supplier model.
    """
    class Meta:
        model = Supplier
        fields = '__all__'  # Include all fields from the Supplier model