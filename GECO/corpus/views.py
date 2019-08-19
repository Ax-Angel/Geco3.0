from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.db import IntegrityError

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.urls import reverse

from corpus.forms import *
from .models import *
from users.models import User

import traceback


# Create your views here.
def index_view(request):
    if request.method == 'GET':
        return render(request, 'index.html', {})

def user_dashboard_view(request):
    if request.user.is_authenticated:
        if request.method == 'GET' and request.GET.get('q',False):
            name_project = str(request.GET.get('q', ''))
            project = Project.objects.get(name_project=name_project)
            print(project)
            documents = Document.objects.filter(project=project)

            result = []
            for doc in documents:
                files = File.objects.filter(document=doc)
                for f in files:
                    result.append(f)
    
        else:
            result = []
            project = None
    else:
        return redirect('login')

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


class Project_Create(CreateView):
    model = Project
    template_name = 'create_project_form.html'
    form_class = create_project_form
    second_form_class = metadata_project_form    
    success_url = reverse_lazy('dashboard')

    #enviar el contexto a la vista
    def get_context_data(self, **kwargs):
        context = super(Project_Create, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        if 'error' not in context:
            context['error'] = False
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object #se accede al objeto
        # se recoge de los 2 formularios la información que se introduce
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        error = ''
        # se validan ambos 2 formularios para poderlos guardar
        if form.is_valid() and form2.is_valid():
            validatedData = form.cleaned_data
            validatedData2 = form2.cleaned_data
            print(validatedData2)
            try:
                p = Project(owner = request.user,
                            name_project = str(validatedData['name_project']),
                            description = str(validatedData['description']),
                            public_status = validatedData['public_status'],
                            collab_status = validatedData['collab_status'],
                            parallel_status = validatedData['parallel_status'])
                p.save()
                p.project_members.add(request.user)

                list_md = validatedData2['name_metadata']
                print(list_md)
                for md in list_md:
                    meta = Metadata.objects.get(id=int(md))
                    meta.project.add(p)
                    meta.save()  
                return HttpResponseRedirect(self.get_success_url()+'?q='+validatedData['name_project'])
            
            except IntegrityError as e:
                error = 'Ya existe un proyecto con ese nombre. Compruebe que sea único.'
                return self.render_to_response(self.get_context_data(form=form, form2=form2, error=error))
        
        else: #en caso de no ser válidos se muestra el contexto en blanco
            return self.render_to_response(self.get_context_data(form=form, form2=form2, error=error))

class Project_Update(UpdateView):
    model = Project
    second_model = Metadata # se llama el segundo modelo
    template_name = 'create_project_form.html'
    form_class = create_project_form
    second_form_class = metadata_project_form    
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs): #para poder llamar los objectos de los modelos y se rendericen los atributos de c/u
        context = super(Project_Update, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0) #se obtienen las llaves
        solicitud = self.model.objects.get(id=pk) #contiene el objeto de la solicitud a editar
        persona = self.second_model.objects.get(id=solicitud.persona_id) #contiene el objeto de Persona relacionada a la solicitud
        if 'form' not in context: #validar que los form esten en el contexto y luego asignarlos
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class(instance=persona) #se instancia a la persona que se obtiene
        context['id'] = pk
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object #se obtiene el objeto
        id_solicitud = kwargs['pk'] #obtiene el id que se envío por url
        solicitud = self.model.objects.get(id=id_solicitud)
        persona = self.second_model.objects.get(id=solicitud.persona_id)
        # se recoge de los 2 formularios la información que se introduce, instanciado
        form = self.form_class(request.POST, instance=solicitud)
        form2 = self.second_form_class(request.POST, instance=persona)
        #se validan los formularios y se guarda la información
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(self.get_success_url())

   # De igual manera, pensar el editar proyecto,! cuando se edita un proyecto
   # verificar que si se editaron los metadatos, entonces esos metadatos si
   # si son nuevos agregarlos en la relación y luego agregarlos en la relacion
   # con los Files-Metadatos con valor nulos!
   # si no son nuevos mantenerlos
   # si los que están no estaban con relación a los anteriores, entonces 
   # borrárlos en la relación Projecto - Metadato y File - Metadato


class Project_Delete(DeleteView):
    model = Project
    template_name = 'delete_project_from.html'
    success_url = reverse_lazy('dashboard')
      
    
#ya esta función no sirve
'''def create_project_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = create_project_form(request.POST)
            form2 = metadata_project_form(request.POST)
            if form.is_valid() and form2.is_valid():
                validatedData = form.cleaned_data
                validatedData2 = form2.cleaned_data
                
                try:
                    p = Project(owner = request.user,
                                name_project = str(validatedData['name_project']),
                                description = str(validatedData['description']),
                                public_status = validatedData['is_public'],
                                collab_status = validatedData['is_collab'],
                                parallel_status = validatedData['is_parallel'])
                    p.save()
                    p.project_members.add(request.user)
                    
                    list_md = validatedData2['name_metadata']
                    for md in list_md:
                        meta = Metadata.objects.get(id=int(md))
                        meta.project.add(p)
                        meta.save()                       
                    return redirect(reverse('dashboard')+'?q='+validatedData['name_project'])
                except IntegrityError as e:
                    #traceback.print_exc()
                    error = 'Compruebe que el nombre y la descripción de su proyecto sean únicos. Ya existe un proyecto con esos valores.'
                    return render(request, 'create_project_form.html', {'form': form, 'form2': form2, 'error': error})
                    #return render(request, 'create_project_form.html', {'form': form, 'form2': form2, 'error': str(traceback.print_exception)})
        else:
            form = create_project_form()
            form2 = metadata_project_form()
    else:
        return redirect('index')
    return render(request, 'create_project_form.html', {'form': form, 'form2': form2, 'error': False})
'''

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
                                        name_file = f.name,
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
                    project = Project.objects.get(name_project = str(validatedData['project_name']))

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


def add_metadata_document(request):
    error=""
    if request.method == 'POST':
        print(request.POST)
        if request.user.is_authenticated:
            try:
                project = Project.objects.get(name_project = str(request.POST['project_name']))
            except:
                error = "Proyecto no encontrado"
                return
            try:
                file = File.objects.get(pk = int(request.POST['document']))
            except:
                error = "Archivo no encontrado"
                return
            try:
                meta = Metadata.objects.get(pk = int(request.POST['metadata']))
            except:
                error = "Metadato no encontrado"
                return
            users = Project.objects.values_list('project_members', flat=True)
            if request.user.pk in users:                
                rel = File_Metadata_Relation(metadata = meta,
                                             file = file,
                                             data_value = str(request.POST['data'])
                    )
                rel.save()
                return redirect('/dashboard/?q='+str(request.POST['project_name']))
                    
    elif request.method == 'GET' and request.GET.get('q',False):
        project = str(request.GET.get('q', ''))
        projectObj = Project.objects.get(name_project=project)
        documents = Document.objects.filter(project=projectObj)
        metadata = Metadata.objects.filter(project=projectObj)

        doc_list = []
        for doc in documents:
            files = File.objects.filter(document=doc)
            for f in files:
                doc_list.append(f)

        tp = []
        for doc in doc_list:
            tp.append((doc.pk, doc.name))
        choices_doc = tuple(tp)

        tp = []
        for md in metadata:
            tp.append((md.pk, md.name))
        choices_md = tuple(tp)

        form = data_document_form(choices_doc=choices_doc, choices_md=choices_md, initial={'project_name': projectObj.name})
    return render(request, 'add_data_document.html', {'form': form, 'error': error})    


def help_view(request):
    if request.method == 'POST':
        form = contact_form(request.POST)
        if form.is_valid():
            validatedData = form.cleaned_data
            name = validatedData['name']
            from_email = validatedData['email']
            message = validatedData['message']
            
            subject='Mensaje de usuario GECO'
            body_message = 'Usted ha recibido un nuevo mensaje de un usuario'+'\n'+'Nombre: '+name+'\n'+'Correo elecrónico: '+from_email+'\n'+'Mensaje: '+message
            email = EmailMessage(subject, body_message, from_email, to=['gil@iingen.unam.mx'], 
                                 reply_to=[from_email])
            email.send()
            
    form = contact_form()
    return render(request, 'help.html', {'form': form})


def apps_view(request):
    return render(request, 'applications.html')