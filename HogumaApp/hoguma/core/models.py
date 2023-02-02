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

