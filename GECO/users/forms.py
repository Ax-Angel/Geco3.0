# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class register_user_form(forms.Form):
    """
    Esta clase define el template para crear usuarios.
    
    El modelo de los usuarios se encuentra en django.contrib.auth.models.user

    """
    username = forms.CharField(label='Nombre de usuario', max_length=100, required=True)
    email = forms.EmailField(max_length=100, label="Correo electrónico", required=True)
    password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña", required=True)
    institution = forms.CharField(max_length=100, label="Institución", required=False)
    degree = forms.CharField(max_length=100, label="Grado escolar", required=False)
    country = forms.CharField(max_length=100, label="País", required=False)