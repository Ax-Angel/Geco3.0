from django.shortcuts import render, redirect, get_object_or_404 # noqa
from users.models import User
from users.forms import *
import traceback

# Create your views here.
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
                return redirect('error')#Falta crear la vista para cuando falla la creacion de usuarios por escribir un nombre de usuario que ya existe
                                        #o en caso de cualquier otro error causado por intentar crear un nuevo usuario
            return redirect('login')
    else:
        form = register_user_form(request.POST)
    return render(request, 'registration/register_user_form.html', {'form': form})

def edit_user_view(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'GET':
        form = EditForm(instance=user)
    else:
        form = EditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
        #  hacer el return
    return render(request, "registration/edit_user.html", {'form': form})