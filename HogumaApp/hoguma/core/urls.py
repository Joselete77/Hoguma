from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import index, reservations, register, bestfood, restaurant, room, reservationRestaurant


urlpatterns = [
    path('', index, name='index'),
    path('reservations/', reservations, name='reservations'),
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='core/logout.html'), name='logout'),
    path('bestfood/',bestfood, name='bestfood'),
    path('restaurant/', restaurant, name='restaurant'),
    path('room/', room, name='room'),
    path('reservationRestaurant/', reservationRestaurant, name='reservationRestaurant'),
]
