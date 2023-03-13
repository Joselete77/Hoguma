from django import forms  
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError  
from .models import Profile
from django.utils.translation import gettext_lazy as _


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label=_('Nombre'), min_length=2, max_length=150)
    last_name = forms.CharField(label=_('Apellidos'), min_length=2, max_length=150)
    email = forms.EmailField(label=_('Correo electrónico'))  
    username = forms.CharField(label=_('Nombre de usuario'), min_length=5, max_length=150)  
    password1 = forms.CharField(label=_('Contraseña'), widget=forms.PasswordInput)  
    password2 = forms.CharField(label=_('Confirmar contraseña'), widget=forms.PasswordInput)  
  
    def clean_username(self):  
        username = self.cleaned_data['username'].lower()  
        new = User.objects.filter(username = username).count()  
        if new > 0:  
            raise ValidationError(_("Este nombre de usuario ya está registrado"))  
        return username  
  
    def clean_email(self):  
        email = self.cleaned_data['email'].lower()  
        new = User.objects.filter(email = email).count()  
        if new > 0:  
            raise ValidationError(_("Este correo electrónico ya está registrado"))  
        return email  
  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError(_("Las contraseñas no coinciden"))  
        return password2  
    
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        return first_name  
  
    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        return last_name
      
    def save(self):  
        user = User.objects.create_user(  
            self.cleaned_data['username'],  
            email = self.cleaned_data['email'],  
            password = self.cleaned_data['password1'],
            first_name = self.cleaned_data['first_name'],
            last_name = self.cleaned_data['last_name']      
        )  
        return user
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name','email', 'username', 'password1', 'password2')

class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : _('Modificar nombre')}))
    last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : _('Modificar apellidos')}))
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : _('Nuevo nombre de usuario')}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : _('Nuevo correo electrónico')}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

class UpdateAvatarUser(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['avatar']
