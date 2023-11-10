from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

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

class Appointments(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    patient = models.ForeignKey(
        'PatientProfile',
        on_delete=models.CASCADE,
        related_name='patient_appointments'
    )
    doctor = models.ForeignKey(
        'DoctorProfile',
        on_delete=models.CASCADE,
        related_name='doctor_appointments'
    )
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Appointment {self.appointment_id} - {self.doctor.user.username} with {self.patient.user.username} on {self.date} at {self.time}"
