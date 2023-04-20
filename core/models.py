"""
This file contains all the classes handled by our application.
"""

from django.db import models
from django.contrib.auth.models import User


class reservationsRestaurant(models.Model):
    email=models.EmailField()
    date=models.DateField()
    hour=models.TimeField()
    people=models.IntegerField()
    allergy=models.BooleanField()

    def __str__(self):
        return self.email    

class reservationsHotel(models.Model):
    email=models.EmailField()
    typeRoom=models.CharField(max_length=50)
    entry_date=models.DateField()
    departure_date=models.DateField()
    guests=models.IntegerField()

class typeRoomHotel(models.Model):
    name=models.CharField(max_length=50)
    type=models.CharField(max_length=50, default=0, verbose_name='Type room')
    capacity=models.IntegerField()
    capacityMax=models.IntegerField()
    img=models.CharField(max_length=250)
    roomAvailable=models.IntegerField()
    price=models.IntegerField()
    description=models.CharField(max_length=300)

    class Meta:
        verbose_name='Type room'
        ordering=['type']
    
    def __str__(self):
        return self.type

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

class promotion(models.Model):
    name=models.CharField(max_length=50)
    typeRoom=models.OneToOneField(typeRoomHotel, on_delete=models.CASCADE)
    description=models.CharField(max_length=250)
    newPrice=models.IntegerField()
    startDate=models.DateField()
    finishDate=models.DateField()

    class Meta:
        ordering=['name']
    
    def __str__(self):
        return self.name

class refund(models.Model):
    email=models.EmailField()
    idReservation=models.IntegerField()
    price=models.IntegerField()
    makeRefund=models.BooleanField(default=False)

    class Meta:
        ordering=['makeRefund']
    
    def __str__(self):
        return self.email

class hotelInformation(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    phone=models.CharField(max_length=11)
    address=models.CharField(max_length=250)
    fax=models.CharField(max_length=11)
    urlWeb=models.CharField(max_length=50)
    latitude=models.FloatField()
    longitude=models.FloatField()

    def __str__(self):
        return self.name
    
class restaurantDetails(models.Model):
    tipeTable=models.CharField(max_length=150)
    capacity=models.IntegerField()
    totalTable=models.IntegerField()

    def __str__(self) -> str:
        return self.tipeTable