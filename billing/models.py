from django.db import models
from patients.models import Patients

class Invoice(models.Model):
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    invoice_date = models.DateField(db_index=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Paid', 'Paid'), ('Cancelled', 'Cancelled')],
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Invoice {self.id} for {self.patient}"