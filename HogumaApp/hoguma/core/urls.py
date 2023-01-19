from django.urls import path
from .views import index, reservations

urlpatterns = [
    path('', index, name='index'),
    path('reservations/', reservations, name='reservations'),
]
