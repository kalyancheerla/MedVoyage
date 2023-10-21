from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class PatientModel(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
