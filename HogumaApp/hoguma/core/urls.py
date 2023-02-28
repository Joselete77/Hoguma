from django.urls import path
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetDoneView
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='core/User/login.html'), name='login'),
    path('logout/', function_logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('changePassword/', changePassword.as_view(), name='changePassword'),
    path('menuRestaurant/', menuRestaurant, name='menuRestaurant'),
    path('restaurant/', restaurant, name='restaurant'),
    path('room/', room, name='room'),
    path('reservationRestaurant/', reservationRestaurant, name='reservationRestaurant'),
    path('reservationsRestaurantUserAnonymous/', reservationsRestaurantUserAnonymous, name='reservationsRestaurantUserAnonymous'),
    path('room/reservationsRoom/<int:id>', reservationsRoom, name='reservationsRoom'),
    path('reservationsRoomForm/<int:id>', reservationsRoom, name='reservationsRoomForm'),
    path('reservationsHotelUser/', reservationsHotelUser, name='reservationsHotelUser'),
    path('reservationsHotelUser/deleteReservationHotel/<int:id>', deleteReservationHotel, name='deleteReservationHotel'), #user registered
    path('reservationsHotelUser/formUpdateReservationHotel/<int:id>', formUpdateReservationHotel, name='formUpdateReservationHotel'), #user registered
    path('searchReservationsHotelAnonymous/deleteReservationHotel/<int:id>', deleteReservationHotel, name='deleteReservationHotel'), #anonymous
    path('searchReservationsHotelAnonymous/formUpdateReservationHotel/<int:id>', formUpdateReservationHotel, name='formUpdateReservationHotel'), #anonymous
    path('searchReservationsHotelAnonymous/', searchReservationsHotelAnonymous, name='searchReservationsHotelAnonymous'), #anonymous
    path('updateReservationHotel/', updateReservationHotel, name='updateReservationHotel'),
    path('reservationsRestaurantUser/', reservationsRestaurantUser, name='reservationsRestaurantUser'),
    path('updateReservationRestaurant/', updateReservationRestaurant, name='updateReservationRestaurant'),
    path('updateReservationRestaurantUserAnonymous/', updateReservationRestaurantUserAnonymous, name='updateReservationRestaurantUserAnonymous'),
    path('searchReservationsRestaurantAnonymous/', searchReservationsRestaurantAnonymous, name='searchReservationsRestaurantAnonymous'), #anonymous
    path('searchReservationsRestaurantAnonymous/deleteReservationRestaurantUserAnonymous/<int:id>', deleteReservationRestaurantUserAnonymous, name='deleteReservationRestaurantUserAnonymous'), #anonymous
    path('searchReservationsRestaurantAnonymous/formUpdateReservationRestaurantUserAnonymous/<int:id>', formUpdateReservationRestaurantUserAnonymous, name='formUpdateReservationRestaurantUserAnonymous'), #anonymous
    path('reservationsRestaurantUser/deleteReservationRestaurant/<int:id>', deleteReservationRestaurant, name='deleteReservationRestaurant'), #user registered
    path('reservationsRestaurantUser/formUpdateReservationRestaurant/<int:id>', formUpdateReservationRestaurant, name='formUpdateReservationRestaurant'), #user registered
    path('updateReservationRestaurantUserAnonymous/deleteReservationRestaurantUserAnonymous/<int:id>', deleteReservationRestaurantUserAnonymous, name='deleteReservationRestaurantUserAnonymous'),
    path('updateReservationRestaurant/deleteReservationRestaurant/<int:id>', deleteReservationRestaurant, name='deleteReservationRestaurant'),
    path('monuments/', monuments, name='monuments'),
    path('contact/', contact, name='contact'),
    path('busStop/', busStop, name='busStop'),
    path('create_checkout_session/', create_checkout_session, name='create_checkout_session'),
    path('successPay/', successPay, name='successPay'),
    path('reservationsRoomPromotion/', reservationsRoomPromotion, name='reservationsRoomPromotion'),
    path('termsAndPrivacity/', termsAndPrivacity, name='termsAndPrivacity'),
    path('successPayRoomReservation/', successPayRoomReservation, name='successPayRoomReservation'),
    path('password-reset/',
         PasswordResetView.as_view(
             template_name='core/User/ResetPassword/password_reset.html',
             subject_template_name='core/User/ResetPassword/password_reset_subject.txt',
             email_template_name='core/User/ResetPassword/password_reset_email.html',
             # success_url='/login/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(
             template_name='core/User/ResetPassword/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name='core/User/ResetPassword/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(
             template_name='core/User/ResetPassword/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]
