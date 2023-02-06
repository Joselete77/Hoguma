from django.urls import path
from django.contrib.auth.views import LoginView
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='core/User/login.html'), name='login'),
    path('logout/', function_logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('changePassword/', changePassword.as_view(), name='changePassword'),
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
    path('reservationsRoom/', reservationsRoom, name='reservationsRoom'),
    path('reservationsHotelUser/', reservationsHotelUser, name='reservationsHotelUser'),
    path('reservationsHotelUser/deleteReservationHotel/<int:id>', deleteReservationHotel, name='deleteReservationHotel'), #user registered
    path('reservationsHotelUser/formUpdateReservationHotel/<int:id>', formUpdateReservationHotel, name='formUpdateReservationHotel'), #user registered
    path('searchReservationsHotelAnonymous/deleteReservationHotel/<int:id>', deleteReservationHotel, name='deleteReservationHotel'), #anonymous
    path('searchReservationsHotelAnonymous/formUpdateReservationHotel/<int:id>', formUpdateReservationHotel, name='formUpdateReservationHotel'), #anonymous
    path('searchReservationsHotelAnonymous/', searchReservationsHotelAnonymous, name='searchReservationsHotelAnonymous'), #anonymous
    path('updateReservationHotel/', updateReservationHotel, name='updateReservationHotel'),
    path('reservationsRestaurantUser/', reservationsRestaurantUser, name='reservationsRestaurantUser'),
    path('updateReservationRestaurant/', updateReservationRestaurant, name='updateReservationRestaurant'),
    path('searchReservationsRestaurantAnonymous/', searchReservationsRestaurantAnonymous, name='searchReservationsRestaurantAnonymous'), #anonymous
    path('searchReservationsRestaurantAnonymous/deleteReservationRestaurant/<int:id>', deleteReservationRestaurant, name='deleteReservationRestaurant'), #anonymous
    path('searchReservationsRestaurantAnonymous/formUpdateReservationRestaurant/<int:id>', formUpdateReservationRestaurant, name='formUpdateReservationRestaurant'), #anonymous
    path('reservationsRestaurantUser/deleteReservationRestaurant/<int:id>', deleteReservationRestaurant, name='deleteReservationRestaurant'), #user registered
    path('reservationsRestaurantUser/formUpdateReservationRestaurant/<int:id>', formUpdateReservationRestaurant, name='formUpdateReservationRestaurant'), #user registered
    path('monuments/', monuments, name='monuments'),
    path('contact/', contact, name='contact'),
    path('busStop/', busStop, name='busStop'),
    path('avatar/', avatar, name='avatar'),
]
