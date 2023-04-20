"""
This file contains the configuration of the administrator user
"""

from django.contrib import admin
from .models import locationBusStop, typeRoomHotel, reservationsHotel, Profile, promotion, refund, hotelInformation, reservationsRestaurant, restaurantDetails

"""
We register the classes that we want to be managed by the administrator
"""
admin.site.register(locationBusStop)
admin.site.register(typeRoomHotel)
admin.site.register(reservationsHotel)
admin.site.register(Profile)
admin.site.register(promotion)
admin.site.register(refund)
admin.site.register(hotelInformation)
admin.site.register(reservationsRestaurant)
admin.site.register(restaurantDetails)

"""
Dashboard customization
"""
admin.site.site_header = 'Hoguma'
admin.site.site_title = 'Hoguma'