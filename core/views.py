"""
This file contains all the logical functions of our application.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.urls import reverse_lazy
from django.contrib.auth.models import User 
from django.utils.translation import get_language, gettext as _
from django.conf import settings
from datetime import datetime, time
import folium
from .forms import CustomUserCreationForm, UpdateUserForm, UpdateAvatarUser
import json
from .models import reservationsRestaurant, reservationsHotel, locationBusStop, typeRoomHotel, Profile, promotion, refund, hotelInformation, restaurantDetails


"""Index redirection code"""
def index(request):
    return render(request, 'core/index.html')

#USER MANAGEMENT

"""Register code"""
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():            

            """
            Creation user
            """            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            form.save()

            user = User.objects.get(username=username)

            """
            #Creation profile
            """             
            avatar = "avatar/default.png" 
            profile = Profile(avatar=avatar, user_id=user.id)
            profile.save()

            message = _('Usuario %(username)s registrado satisfactoriamente.') % {'username' : username}
            messages.success(request, message)
            send_message = EmailMessage("Registro de usuario Hoguma", "{} el registro se ha completado satisfactoriamente, a continuación le proporcionamos sus credenciales: \n \n Usuario: {} \n Contraseña: {} \n \n Muchas gracias, Hoguma.".format(first_name,username, password), 
                                                'hogumahotel@gmail.com', [email]) 
            send_message.send()
            return redirect('index')
    else:
        form = CustomUserCreationForm()

    return render(request,'core/User/register.html',{'form' : form})

"""Logout code"""
def function_logout(request):
    logout(request)
    return redirect('index')

"""Profile code"""
def profile(request):
    now = datetime.now()
    now = now.date()
    allPromotion= promotion.objects.filter(finishDate__gte=now)
    userName = request.user.first_name.split(' ', 1)
    firstNameUser= userName[0]
    username = request.user.username
    email = request.user.email
    
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user, files=request.FILES)
        formAvatar = UpdateAvatarUser(request.POST, instance=request.user.profile, files=request.FILES)
        
        """
        Form to modify user data
        """
        if form.is_valid():
            usernameForm = form.cleaned_data['username']
            emailForm = form.cleaned_data['email']
            usernameBD = User.objects.filter(username=usernameForm).count()
            emailBD = User.objects.filter(email=emailForm).count()

            if usernameBD == 0 or usernameForm == username:
                if emailBD == 0 or emailForm == email:
                    form.save()
                    message = _('Usuario %(username)s modificado satisfactoriamente.') % {'username' : username}
                    messages.success(request, message)
                else:
                    message = _('El correo electrónico introducido ya se encuentra registrado')
                    messages.error(request, message)
            else:
                message = _('El nombre de usuario ya se encuentra registrado')
                messages.error(request, message)
            
            return redirect('profile')

        """
        Form to modify the profile avatar
        """
        if formAvatar.is_valid():
            username = request.user.username
            formAvatar.save()
            message = _('Usuario %(username)s modificado satisfactoriamente.') % {'username' : username}
            messages.success(request, message)
            return redirect('profile')
    else: 
        form = UpdateUserForm()
        formAvatar = UpdateAvatarUser()

    return render(request,'core/User/profile.html',{'allPromotion' : allPromotion, 'form' : form, 'formAvatar' : formAvatar, 'firstNameUser' : firstNameUser})

"""Change password code"""
class changePassword(PasswordChangeView):
    template_name = 'core/User/changePassword.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('index')

#RESTAURANT MANAGEMENT

"""Index restaurant redirection code"""
def restaurant(request):
    return render(request, 'core/Restaurant/indexRestaurant.html')

"""Restaurant menu code"""
def menuRestaurant(request):
    """
    This function collects the information from the JSON files meal and passes it to the template via dictionaries.
    """

    rutaBurger = 'core/static/core/assets/dist/json/burgers.json'
    rutaPizza = 'core/static/core/assets/dist/json/pizzas.json'
    rutaSandwich = 'core/static/core/assets/dist/json/sandwiches.json'
    rutaSteak = 'core/static/core/assets/dist/json/steaks.json'
    rutaBestFood = 'core/static/core/assets/dist/json/best-food.json'
    rutaDessert = 'core/static/core/assets/dist/json/desserts.json'
    rutaDrinks = 'core/static/core/assets/dist/json/drinks.json'
    
    with open(rutaBurger) as contenido:
        document_burger =json.load(contenido)

    with open(rutaPizza) as contenido:
        document_pizza =json.load(contenido)

    with open(rutaSandwich) as contenido:
        document_sandwich=json.load(contenido)

    with open(rutaBestFood) as contenido:
        document_bestFood =json.load(contenido)
    
    with open(rutaDessert) as contenido:
        document_dessert =json.load(contenido)
    
    with open(rutaDrinks) as contenido:
        document_drink =json.load(contenido)

    with open(rutaSteak) as contenido:
        document_steak =json.load(contenido)
    
    return render(request, 'core/Restaurant/menu.html', {'burger' : document_burger, 'pizza' : document_pizza, 'sandwich' : document_sandwich,
                                                        'bestFood' : document_bestFood, 'dessert' : document_dessert, 'drink' : document_drink ,
                                                        'steak' : document_steak, })

"""Restaurant reservation code"""
def reservationRestaurant(request):
    """
    This function is responsible for making reservations in the restaurant if the conditions are met.
    """

    if request.method=='POST':
        """
        We get the data and convert it to the format we want to use
        """
        
        email = request.POST.get('email')
        hour = request.POST.get('hour')
        people = request.POST.get('people')
        allergy = request.POST.get('allergy')
        date = request.POST.get('date')

        parts_date = date.split("-")
        date_convert = "/".join(reversed(parts_date))
        date_convert = datetime.strptime(date_convert,"%d/%m/%Y")
        now = datetime.now()

        hour_convert = datetime.strptime(hour,"%H:%M")
        schedule_work1 = time(9,0)
        schedule_work2 = time(23,45)

        """
        We check the number of people to allocate a table
        """
        if int(people) <= 2:
            restaurantTable = restaurantDetails.objects.get(tipeTable="Table for two")
        else: 
            restaurantTable = restaurantDetails.objects.get(tipeTable="Table for four")
        
        """
        We obtain the number of reservations that are less than or equal to today's date
        """
        reservationsDB = reservationsRestaurant.objects.filter(date__lte = now.date()) 
        reservationsDBCount = reservationsDB.count() 

        """
        We check for reservations that have already ended and delete them
        """
        if reservationsDBCount > 0: 
            for x in reservationsDB: 
                if x.date == now and x.hour < now.hour():           
                    x.delete()
                    restaurantTable.totalTable = restaurantTable.totalTable + 1
                    restaurantTable.save()
                if x.date < now.date():
                    x.delete()
                    restaurantTable.totalTable = restaurantTable.totalTable + 1
                    restaurantTable.save()      

        """
        We check if the reservation meets the conditions of time, date, avalaible tables or if the user already has a reservation
        """
        if now.date() < date_convert.date(): #Check if date is valid
            if hour_convert.time() > schedule_work1 and hour_convert.time() < schedule_work2: #Check if time is valid
                if reservationsRestaurant.objects.filter(email=email, hour=hour, date=date).count() == 1: #Check if the user has a reservation for that moment 
                    message = _('Reserva para el día %(date)s no se ha podido completar. Ya tiene usted una reserva para ese día.') % {'date' : date}
                    messages.error(request, message)                    
                    return redirect(index)
                else:
                    """
                    We check if there are tables available, if so, we make the reservation
                    """
                    
                    if restaurantTable.totalTable > 0: 
                        reservationsRestaurant(date=date, hour=hour, people=people, allergy=allergy, email=email).save()
                        reservation = reservationsRestaurant.objects.get(date=date, hour=hour, people=people, allergy=allergy, email=email)
                        restaurantTable.save()
                        message = _('Mesa reservada satisfactoriamente para el %(date)s a las %(hour)s.') % {'date' : date, 'hour' : hour}
                        messages.success(request, message)
                        send_message = EmailMessage("Mesa reservada correctamente", "Su mesa para {} está reservada para el día {} a las {}.\nCodigo identificador: {} \n \nMuchas gracias, Hoguma.".format(people, date, hour, reservation.id), 
                                                'hogumahotel@gmail.com', [email])
                        send_message.send()

                        restaurantTable.totalTable = restaurantTable.totalTable - 1
                        restaurantTable.save()
                    else:
                        message = _('Para el día %(date)s están todas las mesas ocupadas. Inténtelo con otra fecha.') % {'date' : date}
                        messages.error(request, message)

                    return redirect('index')
            else:
                message = _('Reserva para el día %(date)s no se ha podido completar. Introduzca una hora válida. Horas válidas: 09:00 - 23:45') % {'date' : date}
                messages.error(request, message)    
                return redirect(index)

        else:
            message = _('Reserva para el día %(date)s no se ha podido completar. Introduzca fechas válidas.') % {'date' : date}
            messages.error(request, message)
            return redirect(index)

    else:
        user = request.user
        return render(request, 'core/Restaurant/formReservationRestaurant.html', {'user':user})

"""
Code to obtain user reservations
"""
def reservationsRestaurantUser(request):
    email = request.user.email
    reservationsDB = reservationsRestaurant.objects.filter(email=email)

    return render(request, 'core/Restaurant/reservationsRestaurantUser.html', {'reservationsDB': reservationsDB})

"""
Code to delete user reservations
"""
def deleteReservationRestaurant(request, id):
    reservation=reservationsRestaurant.objects.get(id=id)
    reservation.delete()
    date_reservation = reservation.date

    """
    We check the table type of the reservation
    """
    if int(reservation.people) <= 2: 
        restaurantTable = restaurantDetails.objects.get(tipeTable="Table for two")
    else:
        restaurantTable = restaurantDetails.objects.get(tipeTable="Table for four")

    restaurantTables = restaurantDetails.objects.get(tipeTable=restaurantTable)
    restaurantTables.totalTable = restaurantTables.totalTable + 1
    restaurantTables.save()

    message = _('Reserva para el día %(date)s cancelada correctamente.') % {'date' : date_reservation}
    messages.success(request, message)

    return redirect(reservationsRestaurantUser)

"""
Form code to update a reservation
"""
def formUpdateReservationRestaurant(request, id):
    reservation=reservationsRestaurant.objects.get(id=id)
    
    """
    We perform a data conversion
    """
    if reservation.hour.minute == 0:
        reservation.hour = str(reservation.hour.hour)+':'+str(reservation.hour.minute)+str(0)
    else:
        reservation.hour = str(reservation.hour.hour)+':'+str(reservation.hour.minute)
    reservation.date = str(reservation.date)

    return render(request, 'core/Restaurant/updateReservationRestaurant.html', {'reservation': reservation})

"""
Code to modify a reservation 
"""
def updateReservationRestaurant(request):
    """
    This function is similar to that of making a reservation, but in this the reservation is modified
    """

    id = int(request.POST['id'])
    email = request.POST.get('email')
    hour = request.POST.get('hour')
    people = request.POST.get('people')
    allergy = request.POST.get('allergy')
    date = request.POST.get('date')

    parts_date = date.split("-")
    date_convert = "/".join(reversed(parts_date))
    date_convert = datetime.strptime(date_convert,"%d/%m/%Y")
    now = datetime.now()

    hour_convert = datetime.strptime(hour,"%H:%M")
    schedule_work1 = time(9,0)
    schedule_work2 = time(23,45)

    if int(people) <= 2:
        restaurantTable = restaurantDetails.objects.get(tipeTable="Table for two")
    else: 
        restaurantTable = restaurantDetails.objects.get(tipeTable="Table for four")

    reservationsDB = reservationsRestaurant.objects.filter(date__lte = now.date()) 
    reservationsDBCount = reservationsDB.count()

    if reservationsDBCount > 0:
        for x in reservationsDB: 
            if x.date == now and x.hour < now.hour():         
                x.delete()
                restaurantTable.totalTable = restaurantTable.totalTable + 1 
                restaurantTable.save()
            if x.date < now.date(): 
                x.delete()
                restaurantTable.totalTable = restaurantTable.totalTable + 1
                restaurantTable.save()   

    if date_convert.date() > now.date():
        if hour_convert.time() > schedule_work1 and hour_convert.time() < schedule_work2:
            if restaurantTable.totalTable > 0:
                reservation=reservationsRestaurant.objects.get(id=id)
                reservation.email = email
                reservation.hour = hour
                reservation.people = people
                reservation.allergy = allergy
                reservation.date = date   
                reservation.save()

                send_message = EmailMessage("Reserva de mesa modificada correctamente", "Su mesa para {} está reservada para el día {} a las {}.\nCodigo identificador: {} \n \nMuchas gracias, Hoguma.".format(people, date, hour, reservation.id), 
                                                   'hogumahotel@gmail.com', [email]) 
                send_message.send()
                restaurantTable.totalTable = restaurantTable.totalTable - 1
                restaurantTable.save()
                message = _('Reserva para el día %(date)s modificada correctamente.') % {'date' : date}
                messages.success(request, message)
        else:
            message = _('Reserva para el día %(date)s no se ha podido modificar. Introduzca una hora válida. Horas válidas: 09:00 - 23:45') % {'date' : date}
            messages.error(request, message)           
    else:
        message = _('Reserva para el día %(date)s no se ha podido modificar. Introduzca fechas válidas.') % {'date' : date}
        messages.error(request, message)

    return redirect(index)

#RESTAURANT MANGEMENT ANONYMOUS USERS

"""
Code to obtain anonymous user reservations
"""
def reservationsRestaurantUserAnonymous(request):
    return render(request, 'core/Restaurant/reservationsRestaurantUserAnonymous.html')

"""
Code to search for the reservation of an anonymous user
"""
def searchReservationsRestaurantAnonymous(request):
    if request.method == 'POST':
        id_anonymous = request.POST['id']
        email_anonymous = request.POST['email']
        reservationsDB = reservationsRestaurant.objects.filter(email=email_anonymous, id=id_anonymous)
        if reservationsDB.count() > 0:
            return render(request, 'core/Restaurant/reservationsRestaurantUserAnonymous.html', {'reservationsDB': reservationsDB})
        else:
            return render(request, 'core/Restaurant/searchReservationsRestaurantAnonymous.html')
    else:
        return render(request, 'core/Restaurant/searchReservationsRestaurantAnonymous.html')

"""
Code to delete anonymous user reservations
"""
def deleteReservationRestaurantUserAnonymous(request, id):
    reservation=reservationsRestaurant.objects.get(id=id)
    reservation.delete()
    date_reservation = reservation.date

    if int(reservation.people) <= 2: 
        restaurantTable = restaurantDetails.objects.get(tipeTable="Table for two")
    else:
        restaurantTable = restaurantDetails.objects.get(tipeTable="Table for four")

    restaurantTables = restaurantDetails.objects.get(tipeTable=restaurantTable)
    restaurantTables = restaurantTables + 1
    restaurantTables.save()

    message = _('Reserva para el día %(date)s cancelada correctamente.') % {'date' : date_reservation}
    messages.success(request, message)

    return redirect(index)

"""
Form code to update a reservation
"""
def formUpdateReservationRestaurantUserAnonymous(request, id):
    reservation=reservationsRestaurant.objects.get(id=id)
    if reservation.hour.minute == 0:
        reservation.hour = str(reservation.hour.hour)+':'+str(reservation.hour.minute)+str(0)
    else:
        reservation.hour = str(reservation.hour.hour)+':'+str(reservation.hour.minute)
    reservation.date = str(reservation.date)

    return render(request, 'core/Restaurant/updateReservationRestaurantUserAnonymous.html', {'reservation': reservation})

"""
Code to modify a reservation 
"""
def updateReservationRestaurantUserAnonymous(request):

    id = int(request.POST['id'])
    email = request.POST.get('email')
    hour = request.POST.get('hour')
    people = request.POST.get('people')
    allergy = request.POST.get('allergy')
    date = request.POST.get('date')

    parts_date = date.split("-")
    date_convert = "/".join(reversed(parts_date))
    date_convert = datetime.strptime(date_convert,"%d/%m/%Y")
    now = datetime.now()

    hour_convert = datetime.strptime(hour,"%H:%M")
    schedule_work1 = time(9,0)
    schedule_work2 = time(23,45)

    if date_convert.date() > now.date():
        if hour_convert.time() > schedule_work1 and hour_convert.time() < schedule_work2:
            reservation=reservationsRestaurant.objects.get(id=id)
            reservation.email = email
            reservation.hour = hour
            reservation.people = people
            reservation.allergy = allergy
            reservation.date = date   
            reservation.save()

            send_message = EmailMessage("Reserva de mesa modificada correctamente", "Su mesa para {} está reservada para el día {} a las {}.\nCodigo identificador: {} \n \nMuchas gracias, Hoguma.".format(people, date, hour, reservation.id), 
                            'hogumahotel@gmail.com', [email]) #send email to the customer with the reservation
            send_message.send()
            message = _('Reserva para el día %(date)s modificada correctamente.') % {'date' : date}
            messages.success(request, message)
        else:
            message = _('Reserva para el día %(date)s no se ha podido modificar. Introduzca una hora válida. Horas válidas: 09:00 - 23:45') % {'date' : date}
            messages.error(request, message)           
    else:
        message = _('Reserva para el día %(date)s no se ha podido modificar. Introduzca fechas válidas.') % {'date' : date}
        messages.error(request, message)

    return redirect(index)

#HOTEL MANAGEMENT

"""
Redirection code to the rooms page
"""
def room(request):
    room = typeRoomHotel.objects.all()
    room = room.order_by('id')

    return render(request, 'core/Hotel/room.html', {'room': room})

"""
Code to make a room reservation
"""
def reservationsRoom(request, id):  
    room_selected = typeRoomHotel.objects.get(id=id)
    
    if request.method=='POST':
        email = request.POST.get('email')
        entry_date = request.POST.get('entry_date')
        departure_date = request.POST.get('departure_date')
        guests = request.POST.get('guests')
        roomName = request.POST.get('roomName')
        observations = request.POST.get('observations')
        typeRoom = room_selected.type

        parts_dateEntry = entry_date.split("-")
        dateEntry_convert = "/".join(reversed(parts_dateEntry))
        dateEntry_convert = datetime.strptime(dateEntry_convert,"%d/%m/%Y")

        parts_dateDeparture = departure_date.split("-")
        dateDeparture_convert = "/".join(reversed(parts_dateDeparture))
        dateDeparture_convert = datetime.strptime(dateDeparture_convert,"%d/%m/%Y")

        totalDays = (dateDeparture_convert - dateEntry_convert).days

        now = datetime.now()
        now = now.date()
        roomsAvalaible = typeRoomHotel.objects.get(type=typeRoom)
        price = roomsAvalaible.price

        """
        We store the data in a session to later work with it
        """
        request.session['email'] = email
        request.session['entry_date'] = entry_date
        request.session['departure_date'] = departure_date
        request.session['typeRoom'] = typeRoom
        request.session['price'] = roomsAvalaible.price
        request.session['priceTotal'] = roomsAvalaible.price * totalDays
        request.session['days'] = totalDays
        request.session['guests'] = guests
        request.session['roomName'] = roomName
        request.session['observations'] = observations

        """
        We check if the reservation meets the entry date, departure date, guests or avalaible rooms
        """
        if entry_date < departure_date and dateEntry_convert.date() >= now:
            if int(guests) <= roomsAvalaible.capacityMax:
                if roomsAvalaible.roomAvailable < 1 : #We check if there are no rooms available to see if they may already be vacant
                    roomsAvalaible2 = reservationsHotel.objects.filter(departure_date__lte = now, typeRoom = typeRoom) 
                    countRoom = roomsAvalaible2.count()
                    roomsAvalaible.roomAvailable = roomsAvalaible.roomAvailable + countRoom #We add the rooms already available
                    if countRoom > 0:
                        roomsAvalaible.save()
                        return render(request, 'core/checkoutPayment/checkout.html', {'price' : price, 'totalDays' : totalDays})

                    else:
                        message = _('No se han encontrado habitaciones disponibles para las fechas seleccionadas.')
                        messages.error(request, message)  
                        return redirect(reservationsRoom, id=room_selected.id)
                else:
                    return render(request, 'core/checkoutPayment/checkout.html', {'price' : price, 'totalDays' : totalDays})
            else:
                message = _('ERROR. No pueden ser tantos huéspedes en este tipo de habitación, ¿qué tal si miras otra?')
                messages.error(request, message)  
                return redirect(reservationsRoom, id=room_selected.id)                
        else:
            message = _('ERROR. Las fechas para la reserva deben ser válidas.')
            messages.error(request, message)  
            return redirect(reservationsRoom, id=room_selected.id)
        
    else:
        return render(request, 'core/Hotel/formReservationRoom.html', {'room_selected' : room_selected})

"""
Code to make a room reservation with a promotion
"""
def reservationsRoomPromotion(request):
    """
    This function is the same as the previous one but taking into account the price of the promotion
    """

    if request.method=='POST':
        id = request.POST.get('idTypeRoomForm')
        entry_date = request.POST.get('entry_date')
        departure_date = request.POST.get('departure_date')
        email = request.user.email
        id_promotion = promotion.objects.get(id=id)
        typeRoom = str(id_promotion.typeRoom)
        guests = request.POST.get('guests')
        observations = request.POST.get('observations')
        roomName = id_promotion.name

        parts_dateEntry = entry_date.split("-")
        dateEntry_convert = "/".join(reversed(parts_dateEntry))
        dateEntry_convert = datetime.strptime(dateEntry_convert,"%d/%m/%Y")

        parts_dateDeparture = departure_date.split("-")
        dateDeparture_convert = "/".join(reversed(parts_dateDeparture))
        dateDeparture_convert = datetime.strptime(dateDeparture_convert,"%d/%m/%Y")

        totalDays = (dateDeparture_convert - dateEntry_convert).days

        now = datetime.now()
        now = now.date()
        roomsAvalaible = typeRoomHotel.objects.get(type=typeRoom)
        price = id_promotion.newPrice

        request.session['email'] = email
        request.session['entry_date'] = entry_date
        request.session['departure_date'] = departure_date
        request.session['typeRoom'] = typeRoom
        request.session['price'] = price
        request.session['priceTotal'] = price * totalDays
        request.session['days'] = totalDays
        request.session['guests'] = guests
        request.session['roomName'] = roomName
        request.session['observations'] = observations

        if entry_date < departure_date and dateEntry_convert.date() >= now:
            if int(guests) <= roomsAvalaible.capacityMax:
                if roomsAvalaible.roomAvailable < 1 : #Check if there is any room
                    roomsAvalaible2 = reservationsHotel.objects.filter(departure_date__lte = now, typeRoom = typeRoom) 
                    countRoom = roomsAvalaible2.count()
                    roomsAvalaible.roomAvailable = roomsAvalaible.roomAvailable + countRoom #Add new rooms availables
                    if countRoom > 0:
                        return render(request, 'core/checkoutPayment/checkout.html', {'price' : price, 'totalDays' : totalDays})

                    else:
                        message = _('No se han encontrado habitaciones disponibles para las fechas seleccionadas.')
                        messages.error(request, message)  
                        return redirect(profile)
                else:
                    return render(request, 'core/checkoutPayment/checkout.html', {'price' : price, 'totalDays' : totalDays})
            else:
                message = _('ERROR. No pueden ser tantos huéspedes en este tipo de habitación, ¿qué tal si miras otra?')
                messages.error(request, message)  
                return redirect(profile)                
        else:
            message = _('ERROR. Las fechas para la reserva deben ser válidas.')
            messages.error(request, message)  
            return redirect(profile)
        
    else:
        return render(request, 'core/Hotel/formReservationRoom.html')

"""
Code to redirect to the checkout, where the payment is made
"""
def create_checkout_session(request):
    return render(request, 'core/checkoutPayment/checkout.html')

"""
Code that performs the necessary operations when completing the payment
"""
def successPay(request):
    
    """
    We collect the variables stored in the sessions previously
    """
    email = request.session['email']
    entry_date = request.session['entry_date']
    departure_date = request.session['departure_date']
    typeRoom = request.session['typeRoom']
    guests = request.session['guests']
    roomName = request.session['roomName']
    observations = request.session['observations']

    roomsAvalaible = typeRoomHotel.objects.get(type=typeRoom)
    roomsAvalaible.roomAvailable = roomsAvalaible.roomAvailable - 1 
    roomsAvalaible.save()

    reservationsHotel(email=email, entry_date=entry_date, departure_date=departure_date, typeRoom=typeRoom, guests=guests, observations=observations).save()
    reservation = reservationsHotel.objects.get(email=email, entry_date=entry_date, departure_date=departure_date, typeRoom=typeRoom, guests=guests)
    messages.success(request, 'Habitación reservada satisfactoriamente desde el '+entry_date+' hasta el '+departure_date+'.')
    send_message = EmailMessage("Habitación reservada correctamente", "{} para {}, reservada desde el día {} hasta el {}.\nCodigo identificador: {} \n \nMuchas gracias, Hoguma.".format(roomName ,guests, entry_date, departure_date, reservation.id), 
                                'hogumahotel@gmail.com', [email]) 
    send_message.send()

    """
    We delete the sessions because we don't need them
    """
    del request.session['email']
    del request.session['entry_date']
    del request.session['departure_date']
    del request.session['typeRoom']
    del request.session['price']
    del request.session['priceTotal']
    del request.session['days']
    del request.session['guests']
    del request.session['roomName']
    del request.session['observations']

    return redirect(index)

"""
Code to obtain user reservations
"""
def reservationsHotelUser(request):
    email = request.user.email
    reservationsDB = reservationsHotel.objects.filter(email=email)
    
    """
    We filter the rooms to identify the type of room of the reservation
    """
    for x in reservationsDB:
        if x.typeRoom == 'singleRoom':          
            typeRoom = typeRoomHotel.objects.get(type=x.typeRoom)
            x.typeRoom = typeRoom.name
        if x.typeRoom == 'doubleRoom':          
            typeRoom = typeRoomHotel.objects.get(type=x.typeRoom)
            x.typeRoom = typeRoom.name
        if x.typeRoom == 'tripleRoom':          
            typeRoom = typeRoomHotel.objects.get(type=x.typeRoom)
            x.typeRoom = typeRoom.name
        if x.typeRoom == 'suiteRoom':          
            typeRoom = typeRoomHotel.objects.get(type=x.typeRoom)
            x.typeRoom = typeRoom.name
    
    reservationsDB.typeRoom = typeRoom.type
    
    return render(request, 'core/Hotel/reservationsHotelUser.html', {'reservationsDB': reservationsDB})

"""
Code to delete user reservations
"""
def deleteReservationHotel(request, id):
    reservation=reservationsHotel.objects.get(id=id)
    email=reservation.email
    date_entry=reservation.entry_date
    date_departure=reservation.departure_date
    typeRoom=reservation.typeRoom
    room=typeRoomHotel.objects.get(type=typeRoom)
    nameRoom=room.name
    reservation.delete()

    days = (date_departure - date_entry).days
    roomType = typeRoomHotel.objects.get(type=typeRoom)
    price = roomType.price * days
    refund(email=email, idReservation=id, price=price).save()

    message = _('%(nameRoom)s para el día %(date_entry)s cancelada correctamente. Para el reembolso nuestro equipo técnico se pondrá en contacto con usted.') % {'nameRoom' :nameRoom ,'date_entry' : date_entry}
    messages.success(request, message)

    return redirect(index)

"""
Form code to update a reservation
"""
def formUpdateReservationHotel(request, id):
    reservation=reservationsHotel.objects.get(id=id)
    reservation.entry_date = str(reservation.entry_date)
    reservation.departure_date = str(reservation.departure_date)

    room = typeRoomHotel.objects.get(type=reservation.typeRoom) 

    return render(request, 'core/Hotel/updateReservationHotel.html', {'reservation': reservation, 'room' : room})

"""
Code to modify a reservation 
"""
def updateReservationHotel(request):
    """
    This function is similar to that of making a reservation, but in this the reservation is modified
    """
        
    idRoom = int(request.POST['id'])
    email = request.POST['email']
    entry_date = request.POST['entry_date']
    departure_date = request.POST['departure_date']
    typeRoom = request.POST['typeRoom']
    guests = request.POST['guests']
    observations = request.POST['observations']
    room=typeRoomHotel.objects.get(type=typeRoom)
    nameRoom=room.name
    price = room.price

    parts_dateEntry = entry_date.split("-")
    dateEntry_convert = "/".join(reversed(parts_dateEntry))
    dateEntry_convert = datetime.strptime(dateEntry_convert,"%d/%m/%Y")

    parts_dateDeparture = departure_date.split("-")
    dateDeparture_convert = "/".join(reversed(parts_dateDeparture))
    dateDeparture_convert = datetime.strptime(dateDeparture_convert,"%d/%m/%Y")

    totalDaysNew = (dateDeparture_convert - dateEntry_convert).days

    reservation=reservationsHotel.objects.get(id=idRoom)
    entry_date_reservation=reservation.entry_date
    departure_date_reservation=reservation.departure_date
    totalDaysReservation = (departure_date_reservation - entry_date_reservation).days
    
    totalDays= totalDaysNew-totalDaysReservation
    priceTotal = price * totalDays

    request.session['email'] = email
    request.session['entry_date'] = entry_date
    request.session['departure_date'] = departure_date
    request.session['typeRoom'] = typeRoom
    request.session['price'] = price
    request.session['priceTotal'] = priceTotal
    request.session['days'] = totalDays
    request.session['guests'] = guests
    request.session['roomName'] = nameRoom
    request.session['idRoom'] = idRoom
    request.session['observations'] = observations

    now = datetime.now()

    if entry_date < departure_date and dateEntry_convert.date() > now.date():

        """
        We check if the user wants more, less or the same days when modifying the reservation
        """
        if totalDaysNew < totalDaysReservation:
            priceTotal = abs(priceTotal)   
            if refund.objects.filter(idReservation=idRoom).count() > 0:
                refundRoom=refund.objects.get(idReservation=idRoom)
                refundRoom.price = refundRoom.price + priceTotal
                refundRoom.save()
            else:
                refund(email=email, idReservation=idRoom, price=priceTotal).save()

            reservation.email = email
            reservation.entry_date = entry_date
            reservation.departure_date = departure_date
            reservation.typeRoom = typeRoom
            reservation.guests = guests
            reservation.observations = observations
            reservation.save()

            message = _('%(nameRoom)s para el día %(entry_date)s modificada correctamente. Para el reembolso nuestro equipo técnico se pondrá en contacto con usted.') % {'nameRoom' :nameRoom ,'entry_date' : entry_date}
            messages.success(request, message)
        
        if totalDaysNew > totalDaysReservation:
            return render(request, 'core/checkoutPayment/checkout_updateRoom.html', {'price' : price, 'totalDays' : totalDays})
        
        if totalDaysNew == totalDaysReservation:
            reservation.email = email
            reservation.entry_date = entry_date
            reservation.departure_date = departure_date
            reservation.typeRoom = typeRoom
            reservation.guests = guests
            reservation.observations = observations
            reservation.save()     
            message = _('%(nameRoom)s para el día %(entry_date)s modificada correctamente.') % {'nameRoom' :nameRoom ,'entry_date' : entry_date}
            messages.success(request, message)
    else:
        message = _('%(nameRoom)s para el día %(entry_date)s no se ha podido modificar. Introduzca fechas válidas.') % {'nameRoom' :nameRoom ,'entry_date' : entry_date}
        messages.error(request, message)

    return render(request, 'core/index.html')

"""
Code that performs the necessary operations when completing the payment by adding more days to the reservation
"""
def successPayRoomReservation(request):
    """
    This function is the same as that of completing payment
    """

    email = request.session['email']
    entry_date = request.session['entry_date']
    departure_date = request.session['departure_date']
    typeRoom = request.session['typeRoom']
    guests = request.session['guests']
    roomName = request.session['roomName']
    idRoom = request.session['idRoom']
    observations = request.session['observations']

    reservation=reservationsHotel.objects.get(id=idRoom)
    reservation.email = email
    reservation.entry_date = entry_date
    reservation.departure_date = departure_date
    reservation.typeRoom = typeRoom
    reservation.guests = guests
    reservation.observations = observations
    reservation.save()

    reservation = reservationsHotel.objects.get(email=email, entry_date=entry_date, departure_date=departure_date, typeRoom=typeRoom, guests=guests)
    send_message = EmailMessage("Habitación reservada modificada correctamente", "{} para {}, reservada desde el día {} hasta el {}.\nCodigo identificador: {} \n \nMuchas gracias, Hoguma.".format(roomName ,guests, entry_date, departure_date, reservation.id), 
                                'hogumahotel@gmail.com', [email])
    send_message.send()

    message = _('%(nameRoom)s para el día %(entry_date)s modificada y pagada correctamente.') % {'nameRoom' :roomName ,'entry_date' : entry_date}
    messages.success(request, message)   

    del request.session['email']
    del request.session['entry_date']
    del request.session['departure_date']
    del request.session['typeRoom']
    del request.session['price']
    del request.session['priceTotal']
    del request.session['days']
    del request.session['guests']
    del request.session['roomName']
    del request.session['observations']

    return redirect(index)

#HOTEL MANAGEMENT ANONYMOUS USERS

"""
Code to search for the reservation of an anonymous user
"""
def searchReservationsHotelAnonymous(request):
    if request.method == 'POST':
        id_anonymous = request.POST['id']
        email_anonymous = request.POST['email']
        reservationsDB = reservationsHotel.objects.filter(email=email_anonymous, id=id_anonymous)
        
        if reservationsDB.count() > 0:
            for x in reservationsDB:
                if x.typeRoom == 'singleRoom':          
                    typeRoom = typeRoomHotel.objects.get(type=x.typeRoom)
                    x.typeRoom = typeRoom.name
                if x.typeRoom == 'doubleRoom':          
                    typeRoom = typeRoomHotel.objects.get(type=x.typeRoom)
                    x.typeRoom = typeRoom.name
                if x.typeRoom == 'tripleRoom':          
                    typeRoom = typeRoomHotel.objects.get(type=x.typeRoom)
                    x.typeRoom = typeRoom.name
                if x.typeRoom == 'suiteRoom':          
                    typeRoom = typeRoomHotel.objects.get(type=x.typeRoom)
                    x.typeRoom = typeRoom.name
            reservationsDB.typeRoom = typeRoom.type
            return render(request, 'core/Hotel/reservationsHotelUser.html', {'reservationsDB': reservationsDB})
        
        else:
            return render(request, 'core/Hotel/searchReservationsHotelAnonymous.html')
    
    else:
        return render(request, 'core/Hotel/searchReservationsHotelAnonymous.html')

#MANAGEMENT OF DIFFERENT INFORMATION

"""
Code to extract the information from a JSON
"""
def monuments(request):
    """
    We check the language to extract one or the other JSON
    """

    if get_language() == ("es"):
        ruta = 'core/static/core/assets/dist/json/monumentos.json'
        with open(ruta) as contenido:
            document_json =json.load(contenido)
    else:
        ruta = 'core/static/core/assets/dist/json/monuments.json'
        with open(ruta) as contenido:
            document_json =json.load(contenido)

    return render(request, 'core/differentInformation/monuments.html', {'monuments': document_json}) 

"""
Code to send the message of the contact form
"""
def contact(request):
    hotel = hotelInformation.objects.get(id=1) #We identify our hotel with the ID

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subjectEmail = request.POST['subjectEmail']
        messageEmail = 'Mensaje: ' + request.POST['messageEmail'] + ' ' + '\nEmail del remitente: ' + email + '\nNombre del remitente: ' + name
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['hogumahotel@gmail.com']

        send_message = EmailMessage(subjectEmail, messageEmail, email_from ,recipient_list)
        send_message.send()    
        message = _('Mensaje enviado correctamente. Nos pondremos en contacto con usted lo antes posible.')
        
        if messages.success(request, message):
            return redirect('index')
        
        else:
            message = _('ERROR. El mensaje no se ha podido enviar.')
            messages.error(request, message)
            return redirect(contact)
    
    else:
        return render(request, 'core/differentInformation/contact.html', {'hotel' : hotel})

"""
Code to show bus stops on the map
"""
def busStop(request):
    hotel = hotelInformation.objects.get(id=1) #We identify our hotel with the ID
    locations = locationBusStop.objects.all()
    initialMap = folium.Map(location=[hotel.latitude,hotel.longitude], zoom_start=17)
    coordinates_initial = (hotel.latitude,hotel.longitude)

    """
    We add a marker of the hotel location
    """
    folium.Marker(
    location=coordinates_initial,
    popup=folium.Popup(_('¡Usted se encuentra aquí!'), max_width=300),
    icon=folium.Icon(color="red", icon="home"), 
    ).add_to(initialMap)

    """
    We add the markers of the bus stops.
    """
    for location in locations:
        coordinates = (location.latitude, location.longitude)
        folium.Marker(
            location=coordinates,
            popup=folium.Popup(_('Parada de autobús: ') + location.name, max_width=300),
            icon=folium.Icon(color="blue", icon="bus", prefix='fa'), 
        ).add_to(initialMap)

    context = {'map' : initialMap._repr_html_(), 'locations': locations}

    return render(request, 'core/differentInformation/busStop.html', context)

"""
Code to show all the promotions available in the user's profile
"""
def promotions(request):
    now = datetime.now()
    now = now.date()
    allPromotion= promotion.objects.filter(finishDate__lte=now)

    return render(request, 'core/User/profile.html', {'allPromotion' : allPromotion})

"""
Code to show the privacy terms of the hotel
"""
def termsAndPrivacity(request):
    hotel = hotelInformation.objects.get(id=1) #We identify our hotel with the ID

    return render(request, 'core/webPolicy/privacyPolicy.html', {'hotel' : hotel})