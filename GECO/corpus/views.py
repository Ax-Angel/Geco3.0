from django.shortcuts import render, redirect
from corpus.forms import *
from .models import *
from django.db import IntegrityError
import traceback
from users.models import User
from django.views.generic.edit import FormView

# Create your views here.
def index_view(request):
    if request.method == 'GET':
        return render(request, 'index.html', {})

def user_dashboard_view(request):
    if request.method == 'GET' and request.GET.get('p',False):
        project = str(request.GET.get('p', ''))
        projectObj = NormalProject.objects.get(name=project)
        documents = Document.objects.filter(project=projectObj)
        print(documents)
        result = []
        for doc in documents:
            result.append(doc)
    else:
        result = []
        project = None
 
    return render(request, 'user_dashboard.html', {'project': project, 'documents': result})


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

class document_view(FormView): 
    form_class = document_form
    template_name = 'document_form.html'  # Replace with your template.
    success_url = 'http://localhost:8000/dashboard/'  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('files')
        if request.user.is_authenticated:
            users = NormalProject.objects.values_list('project_members', flat=True)
            if request.user.pk in users:
                if form.is_valid():
                    project = NormalProject.objects.get(name=str(form.cleaned_data['project_name']))
                    for f in files:
                        try:
                            doc = Document(file = f,
                                            name = f.name,
                                            owner = request.user,
                                            project = project)
                            doc.save()

                        except:
                            print('error')
                    return self.form_valid(form)

                else:
                    print(form.errors)
                    return self.form_invalid(form)

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if request.user.is_authenticated:
            return super(document_view, self).get(request, *args, **kwargs)
        else:
            redirect('http://localhost:8000/accounts/login/')


def list_collaborators_project_view(request):
    pass


def list_user_projects_view(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            projects = NormalProject.objects.filter(project_members=request.user)
            result = []
            for project in projects:
                result.append(project)
            print(result)       
    else:
        result = []

    return render(request, 'list_user_projects.html', {'result': result})

def add_collaborator_view(request):
    if request.method == 'POST':
        form = add_collaborator_form(request.POST)
        if request.user.is_authenticated:
            if form.is_valid():
                validatedData = form.cleaned_data
                print(validatedData)

                try:
                    project = NormalProject.objects.get(name = str(validatedData['project_name']))

                except:
                    error = "Proyecto no encontrado"

                if project.owner == request.user:
                    try:
                        user = User.objects.get(email = str(validatedData['project_member']))
                        error = ""

                    except:
                        
                        error = "usuario no encontrado"

                    project.project_members.add(user)
    else:
        error = ""
        form = add_collaborator_form()
    return render(request, 'add_collaborator_form.html', {'form': form, 'error': error})