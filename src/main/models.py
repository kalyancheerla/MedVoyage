from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class PatientModel(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)

    LOGIN_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('staff', 'Staff'),
    )
    login_type = models.CharField(max_length=10, choices=LOGIN_CHOICES, default='patient')
    security_question = models.CharField(max_length=86, blank=True, null=True)

class AppointmentModel():
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    patient_id = models.CharField()