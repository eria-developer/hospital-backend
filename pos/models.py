from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()


class Sale(models.Model):
    """
    Model representing a sales transaction in the POS system.
    """
    date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cashier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Sale {self.id} on {self.date}"


class SaleDetail(models.Model):
    """
    Model representing individual products within a sale.
    """
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=False)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        """
        Automatically calculate and set the subtotal before saving.
        """
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)