from django.db import models

class Supplier(models.Model):
    """
    Model representing a supplier in the hospital management system.
    """
    name = models.CharField(max_length=100)
    contact_info = models.TextField(blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        """
        Return a string representation of the supplier.
        """
        return self.name