from django.db import models
# Create your models here.


class users(models.Model):
    name=models.TextField(max_length=30)
    surname=models.TextField(max_length=70)
    email=models.EmailField()
    password=models.TextField(max_length=30)
    username=models.TextField(max_length=30)

