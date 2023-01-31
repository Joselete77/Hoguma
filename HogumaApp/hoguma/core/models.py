from django.db import models
# Create your models here.


class users(models.Model):
    name=models.TextField(max_length=30)
    surname=models.TextField(max_length=70)
    email=models.EmailField()
    password=models.TextField(max_length=30)
    username=models.TextField(max_length=30)

class reservationsRestaurant(models.Model):
    email=models.EmailField()
    date=models.DateField()
    hour=models.TimeField()
    people=models.IntegerField()
    allergy=models.BooleanField()

class reservationsHotel(models.Model):
    email=models.EmailField()
    typeRoom=models.CharField(max_length=50)
    entry_date=models.DateField()
    departure_date=models.DateField()

class typeRoom(models.Model):
    type=models.CharField(max_length=50)
    capacity=models.IntegerField()
    price=models.IntegerField()