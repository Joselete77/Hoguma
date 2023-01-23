from django import forms
from django.db import models
# Create your models here.


class users(models.Model):
    name=models.CharField(max_length=30)
    surname=models.CharField(max_length=70)
    email=models.EmailField()
    password=models.CharField(max_length=30)

class register_user(forms.Form):
    name=forms.CharField(max_length=30)
    surname=forms.CharField(max_length=70)
    email=forms.EmailField()
    password=forms.CharField(max_length=30)