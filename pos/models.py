from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product
from patients.models import Patients

User = get_user_model()

class Sale(models.Model):
    """
    Model representing a sales transaction in the POS system.
    """
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )

    PAYMENT_METHOD_CHOICES = (
        ('CASH', 'Cash'),
        ('CREDIT_CARD', 'Credit Card'),
        ('MOBILE_PAYMENT', 'Mobile Payment'),
        ('INSURANCE', 'Insurance'),
    )

    date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Discount applied to the total amount")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, null=True, blank=True)
    cashier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sales')
    patient = models.ForeignKey(
        Patients,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The patient associated with this sale; null if not specified"
    )

    def __str__(self):
        return f"Sale {self.id} on {self.date} ({self.status})"

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

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Sale {self.sale.id}"