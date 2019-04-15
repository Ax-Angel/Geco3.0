# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class register_user_form(forms.Form):
    """
    Esta clase define el template para crear usuarios.
    
    El modelo de los usuarios se encuentra en django.contrib.auth.models.user

    """
    user_name = forms.CharField(label='Nombre de usuario', max_length=100)
    email = forms.EmailField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())