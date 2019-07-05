# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class register_user_form(forms.Form):
    """
    Esta clase define el template para crear usuarios.
    
    El modelo de los usuarios se encuentra en django.contrib.auth.models.user

    """
    username = forms.CharField(label='Nombre de usuario', max_length=100)
    email = forms.EmailField(max_length=100, label="Correo electrónico")
    password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña")
    institution = forms.CharField(max_length=100, label="Institución")
    degree = forms.CharField(max_length=100, label="Grado escolar")
    country = forms.CharField(max_length=100, label="País")