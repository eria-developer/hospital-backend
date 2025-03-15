from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)  # e.g., "Pharmaceutical", "Equipment"
    stock_level = models.PositiveIntegerField()
    reorder_threshold = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name