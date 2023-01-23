from django.shortcuts import render
from django.http import HttpResponse
from .models import users
from .models import register_user
from django import forms
# Create your views here.

def index(request):
    return render(request, 'core/index.html')

def reservations(request):
    return render(request, 'core/reservations.html')

def rooms(request):
    return render(request, 'core/rooms.html')

def signUp(request):
    return render(request, 'core/signUp.html')

def register(request):

    form = register_user()

    if request.method == "POST":
        form = register_user(request.POST)

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