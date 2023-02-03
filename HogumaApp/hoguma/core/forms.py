from django import forms  
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError  

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label='Nombre', min_length=2, max_length=150)
    last_name = forms.CharField(label='Apellido', min_length=2, max_length=150)
    email = forms.EmailField(label='Correo electrónico')  
    username = forms.CharField(label='Nombre de usuario', min_length=5, max_length=150)  
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)  
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)  
  
    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        new = User.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("User Already Exist")  
        return username  
  
    def email_clean(self):  
        email = self.cleaned_data['email'].lower()  
        new = User.objects.filter(email=email)  
        if new.count():  
            raise ValidationError(" Email Already Exist")  
        return email  
  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Password don't match")  
        return password2  
    
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        return first_name  
  
    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        return last_name
      
    def save(self, commit = True):  
        user = User.objects.create_user(  
            self.cleaned_data['username'],  
            email = self.cleaned_data['email'],  
            password = self.cleaned_data['password1'],
            first_name = self.cleaned_data['first_name'],
            last_name = self.cleaned_data['last_name']      
        )  
        return user

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']
