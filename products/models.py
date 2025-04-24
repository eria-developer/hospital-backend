from django.db import models
from categories.models import Category
from django.core.validators import MinValueValidator

# Create your models here.

class Product(models.Model):
    """
    Model representing a product in a hospital  system.
    
    Tracks essential information about hospital products including:
    - Product details (name, description, etc.)
    - Inventory management (stock level, reorder point)
    - Categorization and tracking information
    """
    category = models.ForeignKey(
        Category, 
        on_delete=models.PROTECT,
        related_name='products',
        help_text="Category this product belongs to"
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    sku = models.CharField(max_length=50, unique=True, help_text="Stock Keeping Unit")
    unit_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    stock_level = models.PositiveIntegerField(
        default=0,
        help_text="Current quantity available in inventory"
    )
    reorder_point = models.PositiveIntegerField(
        default=10,
        help_text="Minimum stock level before reordering"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    
    @property
    def needs_reorder(self):
        """
        Check if the product needs to be reordered based on 
        current stock level and reorder point.
        
        Returns:
            bool: True if stock_level is below or equal to reorder_point
        """
        return self.stock_level <= self.reorder_point