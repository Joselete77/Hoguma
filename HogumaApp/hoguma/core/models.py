from django.db import models

# Create your models here.

class users(models.Model):
    nombre=models.CharField(max_length=30)
    apellidos=models.CharField(max_length=70)
    email=models.EmailField()
    password=models.CharField(max_length=30)