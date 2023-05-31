from django.db import models

class Users(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    otp = models.CharField(max_length=6, default='000000')
