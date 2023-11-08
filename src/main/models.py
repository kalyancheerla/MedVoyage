from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    security_question = models.CharField(max_length=86, blank=True, null=True)
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Additional fields for doctor
    specialization = models.CharField(max_length=100,blank=True)
    bio=models.TextField(blank=True)
    availability_hours = models.CharField(max_length=100,blank=True)

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Additional fields for patient
