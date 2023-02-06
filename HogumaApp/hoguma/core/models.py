from django.db import models
from django.contrib.auth.models import User
# Create your models here.

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

class typeRoomHotel(models.Model):
    type=models.CharField(max_length=50, default=0)
    capacity=models.IntegerField()
    roomAvailable=models.IntegerField()
    price=models.IntegerField()

class locationBusStop(models.Model):
    name=models.CharField(max_length=250, verbose_name='Bus stop')
    address=models.CharField(max_length=250, verbose_name='Bus stop address')
    latitude=models.FloatField(verbose_name='Bus stop latitude')
    longitude=models.FloatField(verbose_name='Bus stop longitude')

    class Meta:
        verbose_name='Bus stop'
        ordering=['name']
    
    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar=models.ImageField(upload_to="avatar", null=True)
