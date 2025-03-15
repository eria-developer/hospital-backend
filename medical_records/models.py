from django.db import models
from patients.models import Patient
from doctors.models import Doctor

class Visit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    visit_date = models.DateTimeField(db_index=True)
    symptoms = models.TextField()
    diagnosis = models.TextField()
    treatment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Visit for {self.patient} on {self.visit_date}"

class Prescription(models.Model):
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE)
    medication = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    instructions = models.TextField()

    def __str__(self):
        return f"{self.medication} for {self.visit}"