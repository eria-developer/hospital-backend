
from rest_framework import serializers
from .models import Product, ProductImage
from django.core.files.base import ContentFile
import base64

class ProductImageSerializer(serializers.ModelSerializer):
    """
    Serializer for the ProductImage model.
    
    Handles image uploads and serialization.
    """
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']

    def get_image(self, obj):
        """
        Return the absolute URL for the image.
        
        Args:
            obj: ProductImage instance
            
        Returns:
            str: Absolute URL of the image, or None if no image
        """
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.
    
    Handles validation, conversion of Product instances to/from JSON,
    and business logic related to product management.
    """
    category_name = serializers.SerializerMethodField()
    needs_reorder = serializers.BooleanField(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    default_image = serializers.PrimaryKeyRelatedField(
        queryset=ProductImage.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'category_name', 'name', 
            'description', 'sku', 'unit_price', 'stock_level', 
            'reorder_point', 'needs_reorder', 'is_active',
            'created_at', 'updated_at', 'images', 'default_image'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'needs_reorder', 'images']

    def get_category_name(self, obj):
        """
        Get the name of the product's category.
        
        Args:
            obj: Product instance
            
        Returns:
            str: Name of the category
        """
        return obj.category.name
    
    def validate_sku(self, value):
        """
        Validate SKU format.
        
        Args:
            value (str): SKU value to validate
            
        Returns:
            str: Validated SKU value
            
        Raises:
            serializers.ValidationError: If SKU format is invalid
        """
        value = value.upper()
        if len(value) < 4:
            raise serializers.ValidationError(
                "SKU must be at least 4 characters long."
            )
        return value
    
    def validate(self, data):
        """
        Validate the entire object.
        
        Args:
            data (dict): Dictionary of field values
            
        Returns:
            dict: Validated data
            
        Raises:
            serializers.ValidationError: If validation fails
        """
        if 'reorder_point' in data and 'stock_level' in data:
            if data['reorder_point'] > data['stock_level']:
                raise serializers.ValidationError(
                    {"stock_level": "Stock level should be above the reorder point."}
                )
        
        if 'default_image' in data and data['default_image']:
            if data['default_image'].product != self.instance and 'instance' in self.context:
                raise serializers.ValidationError(
                    {"default_image": "Default image must belong to this product."}
                )
        
        return data

class ProductStockUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating only the stock level of a product.
    
    This serializer provides a controlled way to adjust inventory
    without allowing modification of other product attributes.
    """
    class Meta:
        model = Product
        fields = ['stock_level']

    def validate_stock_level(self, value):
        """
        Validate stock level adjustments.
        
        Args:
            value (int): New stock level value
            
        Returns:
            int: Validated stock level
            
        Raises:
            serializers.ValidationError: If stock level is invalid
        """
        if value < 0:
            raise serializers.ValidationError(
                "Stock level cannot be negative."
            )
        
        if value <= self.instance.reorder_point:
            print(f"WARNING: Product {self.instance.name} (SKU: {self.instance.sku}) "
                  f"is below reorder point. Current stock: {value}")
        
        return value
