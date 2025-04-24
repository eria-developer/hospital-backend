from rest_framework.serializers import ModelSerializer
from .models import Category


class CategorySerializer(ModelSerializer):
    """
    Serializer for the Category model.

    Serializes all fields of the Category model for use in API requests and responses.

    Fields:
        - id (int): The unique identifier of the category (read-only).
        - name (str): The name of the category (required, max 200 characters).
        - description (str): The description of the category (required).

    Usage:
        Used to validate and serialize category data for creating, updating, or retrieving categories.
    """
    class Meta:
        model = Category
        fields = "__all__"