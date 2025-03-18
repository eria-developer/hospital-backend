from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField()

    def __str__(self):
        return self.name
