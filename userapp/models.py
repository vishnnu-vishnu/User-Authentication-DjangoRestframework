from django.db import models


# Create your models here.

class RegisterDB(models.Model):
    name=models.CharField(max_length=50)
    email = models.EmailField(unique=True,max_length=50)
    password=models.CharField(max_length=12)
    is_verified = models.BooleanField(default=0)
