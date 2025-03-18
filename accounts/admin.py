from django.contrib import admin
from .models import CustomUser, PatientProfile, DoctorProfile

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(PatientProfile)
admin.site.register(DoctorProfile)