from django.shortcuts import render, redirect, get_object_or_404 # noqa
from django.urls import reverse

from django.conf import settings
from django.core.mail import send_mail

from users.models import User
from users.forms import *

import traceback

#User Management
def register_user_view(request):
    """
    Esta función regresa el template y controla la vista del formulario para crear usuarios nuevos.

    El formulario se enuentra definido en forms.py, a este le pasamos solamente el request en tipo post que recibimos del explorador web.
    No es necesario estar logueado para crear un usuario.
    El sistema creara una carpeta personal automáticamente para el usuario.

    """
    if request.method == 'POST':
        form = register_user_form(request.POST)
        if form.is_valid():
            try:
                User.objects.create_user(first_name=str(form.cleaned_data['first_name']),
                                         last_name=str(form.cleaned_data['last_name']),
                                         username=str(form.cleaned_data['username']),
                                         email=str(form.cleaned_data['email']),
                                         password=str(form.cleaned_data['password']),
                                         institution=str(form.cleaned_data['institution']),
                                         degree=str(form.cleaned_data['degree']),
                                         country=str(form.cleaned_data['country']),)
            
            except:
                print(traceback.format_exc())
                return redirect(reverse('register') + '?error')#Falta crear la vista para cuando falla la creacion de usuarios por escribir un nombre de usuario que ya existe
                                        #o en caso de cualquier otro error causado por intentar crear un nuevo usuario
            return redirect('login')
        else:
            return redirect(reverse('register') + '?error')
    else:
        form = register_user_form(request.POST)
    return render(request, 'registration/register_user_form.html', {'form': form})


def edit_user_view(request, user_id):
    if request.user.is_authenticated and (int(request.user.pk) == int(user_id)):
        user = User.objects.get(id=user_id)
        if request.method == 'GET':
            form = EditForm(instance=user)
        else:
            form = EditForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect('info_user', user_id)
        return render(request, "registration/edit_user.html", {'form': form})
    else:
        return redirect('login')


def info_user_view(request, user_id):
    if request.user.is_authenticated and (int(request.user.pk) == int(user_id)):
        if request.method == "GET":
            user = User.objects.get(id=user_id)
        return render(request, "info_user.html", {'user': user})
    else:
        return redirect('login')


def invite_user_view(request):
    error = ''
    email = ''
    sbj = '¡GECO te saluda!'
    msg = 'Hola, {0} {1} te invita a que te registres en GECO'.format(request.user.first_name, request.user.last_name,)

    if request.user.is_authenticated:
        if request.method == 'POST':
            email = request.POST['email_user']
            try:
                send_mail(sbj, msg, settings.DEFAULT_FROM_EMAIL, [email])
                error = 'Invitación enviada correctamente al usuario'
                email = ''
            except:
                error = 'Hubo un error al enviar invitación al usuario'
    else:
        return redirect('login')
    
    contexto = {'error': error, 'email': email}
    return render(request, 'invite_user_form.html', contexto)