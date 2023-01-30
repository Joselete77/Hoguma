from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.template import Template
from django.conf import settings
from django.core.mail import EmailMessage
from datetime import datetime, time
from .forms import CustomUserCreationForm
import json
from .models import reservationsRestaurant

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
    return render(request,'core/register.html',{'form' : form})

def login(request):
    return render(request,'core/login.html')

def function_logout(request):
    logout(request)
    return redirect('index')

def restaurant(request):
    return render(request, 'core/indexRestaurant.html')

def room(request):
    ruta = '/home/jose/UCO/TFG/HogumaApp/hoguma/core/static/core/assets/dist/js/rooms.json'
    plantilla = open("/home/jose/UCO/TFG/HogumaApp/hoguma/core/templates/core/room.html")
    template = Template(plantilla.read())
    plantilla.close()

    with open(ruta) as contenido:
        document_json =json.load(contenido)

    return render(request, 'core/room.html', {'room': document_json})

def menuRestaurant(request):
    return render(request, 'core/indexMenuRestaurant.html')

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
                    return render(request, 'core/formReservationRestaurant.html')
                else:
                    reservationsRestaurant(date=date, hour=hour, people=people, allergy=allergy, email=email).save()
                    messages.success(request, 'Mesa reservada satisfactoriamente para el '+date+' a las '+hour+'.')
                    send_message = EmailMessage("Mesa reservada correctamente", "Su mesa para {} está reservada para el día {} a las {}. \n \n Muchas gracias, Hoguma.".format(people, date, hour), 
                                                'hotelhoguma@gmail.com', [email]) #send email to the customer with the reservation
                    send_message.send()
                    return redirect('index')
            else:
                return render(request, 'core/formReservationRestaurant.html')

        else:
            return render(request, 'core/formReservationRestaurant.html')

    else:
        return render(request, 'core/formReservationRestaurant.html')