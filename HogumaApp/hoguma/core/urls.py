from django.urls import path
from .views import index, reservations, rooms, signUp

urlpatterns = [
    path('', index, name='index'),
    path('reservations/', reservations, name='reservations'),
    path('rooms/', rooms, name='rooms'),
    path('signup/', signUp, name='signup')
]
