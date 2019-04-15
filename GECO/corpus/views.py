from django.shortcuts import render, redirect
from corpus.forms import *
from .models import *
from django.db import IntegrityError

# Create your views here.
def index_view(request):
    if request.method == 'GET':
        return render(request, 'index.html', {})

def user_dashboard_view(request):
    if request.method == 'GET':
        return render(request, 'user_dashboard.html', {})


def normal_project_view(request):
    if request.method == 'POST':
        form = normal_project_form(request.POST)
        if request.user.is_authenticated:
            if form.is_valid():
                validatedData = form.cleaned_data
                print(validatedData)

                try:
                    project = NormalProject(owner = request.user,
                                                name = str(validatedData['name']),
                                                public_status = validatedData['is_public'],
                                                collab_status = validatedData['is_collab']
                                                )
                    project.save()
                    project.project_members.add(request.user)
                    return redirect('http://localhost:8000/dashboard/')
                except IntegrityError as e:
                    return render(request, 'normal_project_form.html', {'form': form})
    else:

        form = normal_project_form()
    return render(request, 'normal_project_form.html', {'form': form})