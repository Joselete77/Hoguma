from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.template import Context, Template
from django.template.loader import get_template
import json
from .models import users

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
    plantilla = open("/home/jose/UCO/TFG/HogumaApp/hoguma/core/templates/core/rooms.html")
    template = Template(plantilla.read())
    plantilla.close()

    with open(ruta) as contenido:
        a =json.load(contenido)

    contexto = Context({'room': a})
    documento = template.render(contexto)
    return HttpResponse(documento)

def bestfood(request):
    ruta = '/home/jose/UCO/TFG/HogumaApp/hoguma/core/static/core/assets/dist/js/best-food.json'
    plantilla = open("/home/jose/UCO/TFG/HogumaApp/hoguma/core/templates/core/bestFood.html")
    template = Template(plantilla.read())
    plantilla.close()
    
    with open(ruta) as contenido:
        a =json.load(contenido)


    contexto = Context({'best_food': a})
    documento = template.render(contexto)
    return HttpResponse(documento)
