from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy

# Create your models here.
class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    security_question = models.CharField(max_length=86, blank=True, null=True)
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    # Add below field for 2FA verification
    is_verified = models.BooleanField(default=False)

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Additional fields for doctor
    specialization = models.CharField(max_length=100,blank=True)
    bio=models.TextField(blank=True)
    availability_hours = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return f'Dr. {self.user.get_full_name()}'

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Additional fields for patient

class Appointments(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    booked_date = models.DateTimeField(default=timezone.now)
    # booked_time = models.TimeField(default=timezone.now)
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
    appointment_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Appointment {self.appointment_id} - {self.doctor.user.username} with {self.patient.user.username} on {self.appointment_date} at {self.start_time}"

class AvailableSlot(models.Model):
    doctor = models.ForeignKey('DoctorProfile', on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    unavailable_flag = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.date} {self.start_time} - {self.end_time}"

    def clean(self):
        # Custom validation to ensure that the start time is before the end time
        if self.end_time <= self.start_time:
            raise ValidationError(gettext_lazy('End time must be after start time.'))

    def save(self, *args, **kwargs):
        # Call the custom validation method
        self.clean()
        super().save(*args, **kwargs)
