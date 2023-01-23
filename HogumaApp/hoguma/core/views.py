from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import users


# Create your views here.

def index(request):
    return render(request, 'core/index.html')

def reservations(request):
    return render(request, 'core/reservations.html')

def rooms(request):
    return render(request, 'core/rooms.html')
"""""
def signUp(request):
    return render(request, 'core/signUp.html')

def register(request):

    form = users()

    if request.method == "POST":
        form = users(request.POST)

        if form.is_valid():
            print("Valido")

            user = users()

            user.name = form.cleaned_data['name']
            user.surname = form.cleaned_data['surname']
            user.email = form.cleaned_data['email']
            user.password = form.cleaned_data['password']

            user.save()

        else:    
            print("Invalido")

    return render(request, 'core/signUp.html', { 'form' : form})
"""

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario {username} creado') #no funciona
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request,'core/register.html',{'form' : form})

def login(request):
    return render(request,'core/login.html')
