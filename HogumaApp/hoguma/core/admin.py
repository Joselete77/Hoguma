from django.contrib import admin
from .models import locationBusStop, typeRoomHotel, reservationsHotel, Profile, promotion, refund

# Register your models here.
admin.site.register(locationBusStop)
admin.site.register(typeRoomHotel)
admin.site.register(reservationsHotel)
admin.site.register(Profile)
admin.site.register(promotion)
admin.site.register(refund)


admin.site.site_header = 'Hoguma'
admin.site.site_title = 'Hoguma'