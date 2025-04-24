from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.
    
    Handles validation, conversion of Product instances to/from JSON,
    and business logic related to product management.
    """
    category_name = serializers.SerializerMethodField()
    needs_reorder = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'category', 'category_name', 'name', 
            'description', 'sku', 'unit_price', 'stock_level', 
            'reorder_point', 'needs_reorder', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'needs_reorder']

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
        # Convert SKU to uppercase
        value = value.upper()
        
        # Implement any additional SKU validation logic here
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
        # Ensure reorder_point is less than or equal to stock_level
        if 'reorder_point' in data and 'stock_level' in data:
            if data['reorder_point'] > data['stock_level']:
                raise serializers.ValidationError(
                    {"stock_level": "Stock level should be above the reorder point."}
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
        
        # Log low stock warnings
        if value <= self.instance.reorder_point:
            print(f"WARNING: Product {self.instance.name} (SKU: {self.instance.sku}) "
                  f"is below reorder point. Current stock: {value}")
        
        return value