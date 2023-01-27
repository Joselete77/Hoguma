from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.template import Context, Template
from django.template.loader import get_template
import json
from .models import reservationsRestaurant
# Create your views here.

def index(request):
    return render(request, 'core/index.html')

def reservations(request):
    return render(request, 'core/reservations.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            print(username)
            message = ('Usuario %(username)s registrado satisfactoriamente.') % {'username' : username}
            print(message)
            messages.success(request, message)
            form.save() 
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request,'core/register.html',{'form' : form})

def login(request):
    return render(request,'core/login.html')

def restaurant(request):
    return render(request, 'core/indexRestaurant.html')

def room(request):
    ruta = '/home/jose/UCO/TFG/HogumaApp/hoguma/core/static/core/assets/dist/js/rooms.json'
    plantilla = open("/home/jose/UCO/TFG/HogumaApp/hoguma/core/templates/core/room.html")
    template = Template(plantilla.read())
    plantilla.close()

    with open(ruta) as contenido:
        document_json =json.load(contenido)

    contexto = Context({'room': document_json})
    documento = template.render(contexto)
    return HttpResponse(documento)

def bestfood(request):
    ruta = '/home/jose/UCO/TFG/HogumaApp/hoguma/core/static/core/assets/dist/js/best-food.json'
    plantilla = open("/home/jose/UCO/TFG/HogumaApp/hoguma/core/templates/core/bestFood.html")
    template = Template(plantilla.read())
    plantilla.close()
    
    with open(ruta) as contenido:
        document_json =json.load(contenido)

    contexto = Context({'best_food': document_json})
    documento = template.render(contexto)
    return HttpResponse(documento)

def reservationRestaurant(request):
    if request.method=='POST':
        email = request.POST.get('email')
        date = request.POST.get('date')
        hour = request.POST.get('hour')
        people = request.POST.get('people')
        allergy = request.POST.get('allergy')
        reservationsRestaurant(date=date, hour=hour, people=people, allergy=allergy, email=email).save()
        messages.success(request, 'Mesa reservada satisfactoriamente para el '+date+' a las '+hour+'.')

        return render(request, 'core/index.html')
    else:
        return render(request, 'core/formReservationRestaurant.html')

    



