from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from django.template import Template
from django.conf import settings
from django.core.mail import EmailMessage
from django.urls import reverse_lazy
from datetime import datetime, time
import folium
from .forms import CustomUserCreationForm, UpdateUserForm
import json
from .models import reservationsRestaurant, reservationsHotel, locationBusStop

# Create your views here.

def index(request):
    return render(request, 'core/index.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name'],

            message = ('Usuario %(username)s registrado satisfactoriamente.') % {'username' : username}
            messages.success(request, message)
            form.save()
            send_message = EmailMessage("Registro de usuario Hoguma", "{} el registro se ha completado satisfactoriamente, a continuación le proporcionamos sus credenciales: \n \n Usuario: {} \n Contraseña: {} \n \n Muchas gracias, Hoguma.".format(first_name,username, password), 
                                                'hotelhoguma@gmail.com', [email]) 
            send_message.send()
            return redirect('index')
    else:
        form = CustomUserCreationForm()

    return render(request,'core/User/register.html',{'form' : form})

def login(request):
    return render(request,'core/User/login.html')

def function_logout(request):
    logout(request)
    return redirect('index')

def editProfile(request):
    if request.method == 'POST':
        user = request.user
        form = UpdateUserForm(request.POST, user)
        if form.is_valid():
            username = request.user.username
            form.save()
            message = ('Usuario %(username)s modificado satisfactoriamente.') % {'username' : username}
            messages.success(request, message)
            return redirect('index')
    else:
        form = UpdateUserForm()
        
    return render(request,'core/User/editProfile.html',{'form' : form})

class changePassword(PasswordChangeView):
    template_name = 'core/User/changePassword.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('index')

#RESTAURANT
def restaurant(request):
    return render(request, 'core/Restaurant/indexRestaurant.html')

def menuRestaurant(request):
    return render(request, 'core/Restaurant/indexMenuRestaurant.html')

def drink(request):
    ruta = '/home/jose/UCO/TFG/HogumaApp/hoguma/core/static/core/assets/dist/js/drinks.json'
    plantilla = open("/home/jose/UCO/TFG/HogumaApp/hoguma/core/templates/core/MenuRestaurant/drinks.html")
    template = Template(plantilla.read())
    plantilla.close()
    
    with open(ruta) as contenido:
        document_json =json.load(contenido)
    
    return render(request, 'core/MenuRestaurant/drinks.html', {'drinks': document_json})

def burger(request):
    ruta = '/home/jose/UCO/TFG/HogumaApp/hoguma/core/static/core/assets/dist/js/burgers.json'
    plantilla = open("/home/jose/UCO/TFG/HogumaApp/hoguma/core/templates/core/MenuRestaurant/burger.html")
    template = Template(plantilla.read())
    plantilla.close()
    
    with open(ruta) as contenido:
        document_json =json.load(contenido)
    
    return render(request, 'core/MenuRestaurant/burger.html', {'burger': document_json})

def pizza(request):
    ruta = '/home/jose/UCO/TFG/HogumaApp/hoguma/core/static/core/assets/dist/js/pizzas.json'
    plantilla = open("/home/jose/UCO/TFG/HogumaApp/hoguma/core/templates/core/MenuRestaurant/pizza.html")
    template = Template(plantilla.read())
    plantilla.close()
    
    with open(ruta) as contenido:
        document_json =json.load(contenido)
    
    return render(request, 'core/MenuRestaurant/pizza.html', {'pizza': document_json})

def sandwich(request):
    ruta = '/home/jose/UCO/TFG/HogumaApp/hoguma/core/static/core/assets/dist/js/sandwiches.json'
    plantilla = open("/home/jose/UCO/TFG/HogumaApp/hoguma/core/templates/core/MenuRestaurant/sandwich.html")
    template = Template(plantilla.read())
    plantilla.close()
    
    with open(ruta) as contenido:
        document_json =json.load(contenido)
    
    return render(request, 'core/MenuRestaurant/sandwich.html', {'sandwich': document_json})

def steak(request):
    ruta = '/home/jose/UCO/TFG/HogumaApp/hoguma/core/static/core/assets/dist/js/steaks.json'
    plantilla = open("/home/jose/UCO/TFG/HogumaApp/hoguma/core/templates/core/MenuRestaurant/steak.html")
    template = Template(plantilla.read())
    plantilla.close()
    
    with open(ruta) as contenido:
        document_json =json.load(contenido)
    
    return render(request, 'core/MenuRestaurant/steak.html', {'steak': document_json})

def dessert(request):
    ruta = '/home/jose/UCO/TFG/HogumaApp/hoguma/core/static/core/assets/dist/js/desserts.json'
    plantilla = open("/home/jose/UCO/TFG/HogumaApp/hoguma/core/templates/core/MenuRestaurant/dessert.html")
    template = Template(plantilla.read())
    plantilla.close()
    
    with open(ruta) as contenido:
        document_json =json.load(contenido)
    
    return render(request, 'core/MenuRestaurant/dessert.html', {'dessert': document_json})

def bestfood(request):
    ruta = '/home/jose/UCO/TFG/HogumaApp/hoguma/core/static/core/assets/dist/js/best-food.json'
    plantilla = open("/home/jose/UCO/TFG/HogumaApp/hoguma/core/templates/core/MenuRestaurant/bestFood.html")
    template = Template(plantilla.read())
    plantilla.close()
    
    with open(ruta) as contenido:
        document_json =json.load(contenido)
    
    return render(request, 'core/MenuRestaurant/bestFood.html', {'best_food': document_json})


def reservationRestaurant(request):
    if request.method=='POST':
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

        if now.date() < date_convert.date(): #check if date is valid
            if hour_convert.time() > schedule_work1 and hour_convert.time() < schedule_work2: #check if time is valid
                if reservationsRestaurant.objects.filter(email=email, hour=hour, date=date).count() == 1: #check if the user has a reservation for that moment 
                    return render(request, 'core/Restaurant/formReservationRestaurant.html')
                else:
                    reservationsRestaurant(date=date, hour=hour, people=people, allergy=allergy, email=email).save()
                    reservation = reservationsRestaurant.objects.get(date=date, hour=hour, people=people, allergy=allergy, email=email)
                    messages.success(request, 'Mesa reservada satisfactoriamente para el '+date+' a las '+hour+'.')
                    send_message = EmailMessage("Mesa reservada correctamente", "Su mesa para {} está reservada para el día {} a las {}.\nCodigo identificador: {} \n \nMuchas gracias, Hoguma.".format(people, date, hour, reservation.id), 
                                                'hotelhoguma@gmail.com', [email]) #send email to the customer with the reservation
                    send_message.send()
                    return redirect('index')
            else:
                return render(request, 'core/Restaurant/formReservationRestaurant.html')

        else:
            return render(request, 'core/Restaurant/formReservationRestaurant.html')

    else:
        user = request.user
        return render(request, 'core/Restaurant/formReservationRestaurant.html', {'user':user})

def reservationsRestaurantUser(request):
    email = request.user.email
    reservationsDB = reservationsRestaurant.objects.filter(email=email)
    return render(request, 'core/Restaurant/reservationsRestaurantUser.html', {'reservationsDB': reservationsDB})

def searchReservationsRestaurantAnonymous(request):
    if request.method == 'POST':
        id_anonymous = request.POST['id']
        email_anonymous = request.POST['email']
        reservationsDB = reservationsRestaurant.objects.filter(email=email_anonymous, id=id_anonymous)
        if reservationsDB.count() > 0:
            return render(request, 'core/Restaurant/reservationsRestaurantUser.html', {'reservationsDB': reservationsDB})
        else:
            return render(request, 'core/Restaurant/searchReservationsRestaurantAnonymous.html')
    else:
        return render(request, 'core/Restaurant/searchReservationsRestaurantAnonymous.html')

def deleteReservationRestaurant(request, id):
    reservation=reservationsRestaurant.objects.get(id=id)
    reservation.delete()

    return redirect(index)

def formUpdateReservationRestaurant(request, id):
    reservation=reservationsRestaurant.objects.get(id=id)

    return render(request, 'core/Restaurant/updateReservationRestaurant.html', {'reservation': reservation})

def updateReservationRestaurant(request):
    id = int(request.POST['id'])
    email = request.POST.get('email')
    hour = request.POST.get('hour')
    people = request.POST.get('people')
    allergy = request.POST.get('allergy')
    date = request.POST.get('date')
    print(id)

    reservation=reservationsRestaurant.objects.get(id=id)
    reservation.email = email
    reservation.hour = hour
    reservation.people = people
    reservation.allergy = allergy
    reservation.date = date   
    reservation.save()

    return render(request, 'core/index.html')

#HOTEL
def room(request):
    ruta = '/home/jose/UCO/TFG/HogumaApp/hoguma/core/static/core/assets/dist/js/rooms.json'
    plantilla = open("/home/jose/UCO/TFG/HogumaApp/hoguma/core/templates/core/Hotel/room.html")
    template = Template(plantilla.read())
    plantilla.close()

    with open(ruta) as contenido:
        document_json =json.load(contenido)
    return render(request, 'core/Hotel/room.html', {'room': document_json})

def reservationsRoom(request): #NO ESTÁ ACABADO FALTAN VALIDACIONES
    if request.method=='POST':
        email = request.POST.get('email')
        entry_date = request.POST.get('entry_date')
        departure_date = request.POST.get('departure_date')
        typeRoom = request.POST.get('typeRoom')

        parts_dateEntry = entry_date.split("-")
        dateEntry_convert = "/".join(reversed(parts_dateEntry))
        dateEntry_convert = datetime.strptime(dateEntry_convert,"%d/%m/%Y")

        parts_dateDeparture = departure_date.split("-")
        dateDeparture_convert = "/".join(reversed(parts_dateDeparture))
        dateDeparture_convert = datetime.strptime(dateDeparture_convert,"%d/%m/%Y")

        reservationsHotel(email=email, entry_date=entry_date, departure_date=departure_date, typeRoom=typeRoom).save()
        messages.success(request, 'Habitación reservada satisfactoriamente desde el '+entry_date+' hasta el '+departure_date+'.')
        
        return redirect('index')
    else:
        return render(request, 'core/Hotel/formReservationRoom.html')

def reservationsHotelUser(request):
    email = request.user.email
    reservationsDB = reservationsHotel.objects.filter(email=email)
    return render(request, 'core/Hotel/reservationsHotelUser.html', {'reservationsDB': reservationsDB})

def searchReservationsHotelAnonymous(request):
    if request.method == 'POST':
        id_anonymous = request.POST['id']
        email_anonymous = request.POST['email']
        reservationsDB = reservationsHotel.objects.filter(email=email_anonymous, id=id_anonymous)
        if reservationsDB.count() > 0:
            return render(request, 'core/Hotel/reservationsHotelUser.html', {'reservationsDB': reservationsDB})
        else:
            return render(request, 'core/Hotel/searchReservationsHotelAnonymous.html')
    else:
        return render(request, 'core/Hotel/searchReservationsHotelAnonymous.html')

def deleteReservationHotel(request, id):
    reservation=reservationsHotel.objects.get(id=id)
    reservation.delete()

    return redirect(index)

def formUpdateReservationHotel(request, id):
    reservation=reservationsHotel.objects.get(id=id)

    return render(request, 'core/Hotel/updateReservationHotel.html', {'reservation': reservation})

def updateReservationHotel(request):
    id = int(request.POST['id'])
    email = request.POST['email']
    entry_date = request.POST['entry_date']
    departure_date = request.POST['departure_date']
    typeRoom = request.POST['typeRoom']

    reservation=reservationsHotel.objects.get(id=id)
    reservation.email = email
    reservation.entry_date = entry_date
    reservation.departure_date = departure_date
    reservation.typeRoom = typeRoom
    reservation.save()

    return render(request, 'core/index.html')


def monuments(request):
    ruta = '/home/jose/UCO/TFG/HogumaApp/hoguma/core/static/core/assets/dist/js/monumentos.json'
    plantilla = open("/home/jose/UCO/TFG/HogumaApp/hoguma/core/templates/core/monuments.html")
    template = Template(plantilla.read())
    plantilla.close()

    with open(ruta) as contenido:
        document_json =json.load(contenido)

    return render(request, 'core/monuments.html', {'monuments': document_json}) 

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subjectEmail = request.POST['subjectEmail']
        messageEmail = request.POST['messageEmail'] + ' ' + '\nEmail del remitente: ' + email + '\nNombre del remitente: ' + name
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['hotelhoguma@gmail.com']

        send_message = EmailMessage(subjectEmail, messageEmail, email_from ,recipient_list)
        send_message.send()
        
        return redirect('index')

    else:
        return render(request, 'core/contact.html')
    
def busStop(request):
    locations = locationBusStop.objects.all()
    initialMap = folium.Map(location=[37.6720542,-1.6990989], zoom_start=17)
    coordinates_initial = (37.6720542,-1.6990989)

    folium.Marker(
    location=coordinates_initial,
    popup=folium.Popup('¡Usted se encuentra aquí!', max_width=300),
    icon=folium.Icon(color="red", icon="home"), 
    ).add_to(initialMap)

    for location in locations:
        coordinates = (location.latitude, location.longitude)
        folium.Marker(
            location=coordinates,
            popup=folium.Popup('Parada de autobús: ' + location.name, max_width=300),
            icon=folium.Icon(color="blue", icon="bus", prefix='fa'), 
        ).add_to(initialMap)

    context = {'map' : initialMap._repr_html_(), 'locations': locations}
    return render(request, 'core/busStop.html', context)
