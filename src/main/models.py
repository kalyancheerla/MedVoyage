from django.db import models

class UserModel(models.Model):
    userName = models.CharField(max_length=100)
    Email = models.IntegerField()
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    dateOfBirth = models.DateField()
    password = models.CharField(max_length=100)
    confirm_password = models.CharField(max_length=100)

