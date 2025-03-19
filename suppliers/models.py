from django.db import models

class Supplier(models.Model):
    """
    Model representing a supplier in the hospital management system.
    """
    name = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=30, unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    alternative_phone = models.CharField(max_length=15, null=True)
    address = models.TextField(blank=True)
    description = models.TextField(null=True)

    def __str__(self):
        """
        Return a string representation of the supplier.
        """
        return self.name