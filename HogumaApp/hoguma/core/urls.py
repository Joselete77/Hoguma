from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import index, register, bestfood, restaurant, room, reservationRestaurant, function_logout


urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', function_logout, name='logout'),
    path('bestfood/',bestfood, name='bestfood'),
    path('restaurant/', restaurant, name='restaurant'),
    path('room/', room, name='room'),
    path('reservationRestaurant/', reservationRestaurant, name='reservationRestaurant'),
]
