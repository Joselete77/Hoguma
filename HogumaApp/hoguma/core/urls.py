from django.urls import path
from django.contrib.auth.views import LoginView
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', function_logout, name='logout'),
    path('menuRestaurant/', menuRestaurant, name='menuRestaurant'),
    path('bestfood/',bestfood, name='bestfood'),
    path('drink/', drink, name='drink'),
    path('burger/', burger, name='burger'),
    path('pizza/', pizza, name='pizza'),
    path('sandwich/', sandwich, name='sandwich'),
    path('steak/', steak, name='steak'),
    path('dessert/', dessert, name='dessert'),
    path('restaurant/', restaurant, name='restaurant'),
    path('room/', room, name='room'),
    path('reservationRestaurant/', reservationRestaurant, name='reservationRestaurant'),
]
