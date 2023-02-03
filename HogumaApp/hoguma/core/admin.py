from django.contrib import admin
from .models import locationBusStop, typeRoomHotel, reservationsHotel

# Register your models here.
admin.site.register(locationBusStop)
admin.site.register(typeRoomHotel)
admin.site.register(reservationsHotel)

