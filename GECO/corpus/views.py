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
    if request.user.is_authenticated:
        if request.method == 'GET' and request.GET.get('q',False):
            project = str(request.GET.get('q', ''))
            projectObj = Project.objects.get(name=project)
            print(projectObj)
            documents = Document.objects.filter(project=projectObj)

            result = []
            for doc in documents:
                files = File.objects.filter(document=doc)
                for f in files:
                    result.append(f)
    
        else:
            result = []
            project = None
    else:
        pass

    user_projects = []
    public_projects = []
    all_projects = Project.objects.all()
    for proj in all_projects:
        print(proj.is_public())
        if proj.is_user_collaborator(request.user):
            user_projects.append(proj)
        elif proj.is_public():
            public_projects.append(proj)  

    return render(request, 'user_dashboard.html', {'user_projects': user_projects, 'public_projects': public_projects, 'project': project, 'documents': result})


def normal_project_view(request):
    if request.method == 'POST':
        form = normal_project_form(request.POST)
        if request.user.is_authenticated:
            if form.is_valid():
                validatedData = form.cleaned_data
                print(validatedData)

                try:
                    project = Project(owner = request.user,
                                                name = str(validatedData['name']),
                                                public_status = validatedData['is_public'],
                                                collab_status = validatedData['is_collab']
                                                )
                    project.save()
                    project.project_members.add(request.user)
                    return redirect('http://localhost:8000/dashboard/')
                except IntegrityError as e:
                    traceback.print_exc()
                    return render(request, 'normal_project_form.html', {'form': form, 'error': str(traceback.print_exception)})
    else:

        form = normal_project_form()
    return render(request, 'normal_project_form.html', {'form': form, 'error': False})

class document_view(FormView): 
    form_class = document_form
    template_name = 'document_form.html'  # Replace with your template.
    success_url = 'http://localhost:8000/dashboard/'  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('files')
        if request.user.is_authenticated:
            users = Project.objects.values_list('project_members', flat=True)
            if request.user.pk in users:
                if form.is_valid():
                    project = Project.objects.get(name=str(form.cleaned_data['project_name']))
                    for f in files:
                        try:
                            doc = Document(project=project,
                                                owner=request.user)
                            doc.save()
                            file = File(file = f,
                                            name = f.name,
                                            document = doc)
                            file.save()

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
            projects = Project.objects.filter(project_members=request.user)
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
                    project = Project.objects.get(name = str(validatedData['project_name']))

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