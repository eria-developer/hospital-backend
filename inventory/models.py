from django.db import models
from suppliers.models import Supplier


class Category(models.Model):
    """
    Model representing item categories in the inventory.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    

class Item(models.Model):
    """
    Model representing items in the inventory.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    expiration_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

