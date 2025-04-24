from django.db import models
from patients.models import Patients
from doctors.models import Doctor

class Appointment(models.Model):
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField(db_index=True)
    status = models.CharField(
        max_length=20,
        choices=[('Scheduled', 'Scheduled'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')],
        default='Scheduled'
    )
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient} with {self.doctor} on {self.appointment_date}"