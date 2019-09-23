from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.db import IntegrityError

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.urls import reverse

from django.conf import settings

from django.core.files.storage import default_storage
from django.core.mail import send_mail

from corpus.forms import *
from .models import *
from users.models import User
from zipfile import ZipFile
from glob import glob

import traceback
import os, shutil
import zipfile
import datetime
import random
import string


# Create your views here.
def index_view(request):
    if request.method == 'GET':
        return render(request, 'index.html', {})

def user_dashboard_view(request):
    if request.user.is_authenticated:
        if request.method == 'GET' and request.GET.get('q',False):
            name_project = str(request.GET.get('q', ''))
            project = Project.objects.get(name_project=name_project)
            
            metadata = Metadata.objects.filter(project=project)
            value_metadata = []
            arr_id_metad = []
            for m in metadata:
                value_metadata.append(m.name_metadata)
                arr_id_metad.append((Metadata.objects.get(name_metadata=m.name_metadata)).id)
            
            result = []
            documents = Document.objects.filter(project=project)
            
            for doc in documents:
                array_tmp = []                
                array_tmp.append(doc.id)
                files = File.objects.filter(document=doc)
                ar_tt = []
                for f in files:
                    a_t = [''] * (len(arr_id_metad)+1)
                    a_t[0]= f.name_file
                    relations = File_Metadata_Relation.objects.filter(file=f).order_by('metadata')
                    for r in relations:
                        value = r.data_value
                        if value==None:
                            value=''
                        a_t[arr_id_metad.index(r.metadata_id)+1] = value
                    ar_tt.append(a_t)
                array_tmp.append(ar_tt)
                result.append(array_tmp)
            
            colaboradores = project.project_members.all()
               
        else:
            value_metadata = []
            result = []
            project = None
            colaboradores = []
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

    return render(request, 'user_dashboard.html', {'user_projects': user_projects, 
                                                   'public_projects': public_projects, 
                                                   'project': project, 'value_metadata':value_metadata, 
                                                   'documents': result,
                                                   'colaboradores': colaboradores})

""" def document_view_view(request, document_id):
    if request.method == 'GET':
        doc_lines = []
        file = File.objects.get(id=document_id)
        text = open(os.path.join(settings.MEDIA_ROOT, str(file.file)), 'r').readlines()
        for line in text:
            doc_lines.append(line)
    return render(request, 'document_view.html', {'file':file, 'text':doc_lines}) """


def randomStringDigits(stringLength=8):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))


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
            
            code_random = randomStringDigits()
            _proj = Project.object.filter(code=code_random)
            while _proj.exists():
                code_random = randomStringDigits()
                _proj = Project.object.filter(code=code_random)
                
            try:
                p = Project(owner = request.user,
                            name_project = str(validatedData['name_project']),
                            description = str(validatedData['description']),
                            public_status = validatedData['public_status'],
                            collab_status = validatedData['collab_status'],
                            parallel_status = validatedData['parallel_status']
                            code = code_random)
                p.save()
                p.project_members.add(request.user)

                list_md = validatedData2['name_metadata']
                for md in list_md:
                    meta = Metadata.objects.get(id=int(md))
                    meta.project.add(p)
                    meta.save()  
                
                new_dir_path = 'mediafiles/'+str(code_random)
                os.makedirs(new_dir_path)
                return HttpResponseRedirect(self.get_success_url()+'?q='+validatedData['name_project'])
            
            except IntegrityError as e:
                traceback.print_exc()
                return self.render_to_response(self.get_context_data(form=form, form2=form2, error=str(traceback.print_exception)))
        
        else: #en caso de no ser válidos se muestra el contexto en blanco
            error = 'Ya existe un proyecto con ese nombre. Compruebe que sea único.'
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
        project = self.model.objects.get(id=pk) #contiene el objeto de la solicitud a editar
        metadata = self.second_model.objects.get(project=project.id) #contiene el objeto de Persona relacionada a la solicitud
        if 'form' not in context: #validar que los form esten en el contexto y luego asignarlos
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class(instance=metadata) #se instancia a la persona que se obtiene
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
    template_name = 'delete_project_form.html'
    success_url = reverse_lazy('dashboard')
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object #se obtiene el objeto
        id_project = kwargs['pk'] #obtiene el id que se envío por url
        project = self.model.objects.get(id=id_project)
        folder = 'mediafiles/'+project.code
        try:
            shutil.rmtree(folder, ignore_errors=True)
        except OSError as e:
            print(e)
        
        project.delete() 
        return HttpResponseRedirect(self.get_success_url())
    

class Document_Delete(DeleteView):
    model = Document
    template_name = 'delete_document_form.html'
    success_url = reverse_lazy('dashboard')
    
    def get_context_data(self, **kwargs):
        context = super(Document_Delete, self).get_context_data(**kwargs)
        self.object = self.get_object #se obtiene el objeto
        document = kwargs['object'] #obtiene el id que se envío por url
        #document = self.model.objects.get(id=id_document)
        project = Project.objects.get(id=document.project_id) 
        files = File.objects.filter(document_id=document.id)
        _f = ''
        for f in files:
            _f+= '"'+f.name_file + '" '
        if 'project' not in context:
            context['project'] = project
        if 'files' not in context:
            context['files'] = _f
    
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object #se obtiene el objeto
        id_document = kwargs['pk'] #obtiene el id que se envío por url
        document = self.model.objects.get(id=id_document)
        
        files = File.objects.filter(document_id=document.id)
        for f in files:
            if os.path.exists(f.file.path):
                os.remove(f.file.path)
        project = Project.objects.get(id=document.project_id)        
        document.delete() 
        return HttpResponseRedirect(self.get_success_url()+'?q='+project.name_project)
    

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


def upload_document_view(request, id_project):
    project = Project.objects.get(id=id_project)
    metadata = Metadata.objects.filter(project = id_project)
    error = ''
    lengua = lenguas()
    
    if request.user.is_authenticated and project.is_user_collaborator(request.user):
        if request.method == 'POST':
            i = 1
            while str(i) in request.POST:
                _file = request.FILES['file_'+str(i)]
                file_name = _file.name
                if not file_name.endswith('.txt'):
                    error = 'Los archivos tienen que ser formato .txt'
                    contexto = {'project':project, 'metadata': metadata, 'error': error, 'lenguas':lengua}
                    return render(request, 'upload_document_form.html', contexto)
                i+=1
            
            if project.parallel_status:
                i = 1
                num_line_tmp = -1
                while str(i) in request.POST:
                    _file = request.FILES['file_'+str(i)]
                    num_line = len(_file.read().splitlines())
                    if i==1:
                        num_line_tmp = num_line
                    else:
                        if num_line_tmp != num_line:
                            error = 'Los corpus paralelos tienen que estar alineados'
                            contexto = {'project':project, 'metadata': metadata, 'error': error, 'lenguas':lengua}
                            return render(request, 'upload_document_form.html', contexto)      
                    i+=1
            
            i = 1
            d = Document(project = project, owner = request.user)
            guarde = False            
            while str(i) in request.POST:
                
                if guarde==False and project.parallel_status:
                    d.save()
                    guarde = True
                elif not project.parallel_status:
                    d = Document(project = project, owner = request.user)
                    d.save()
                            
                _file = request.FILES['file_'+str(i)]
                
                #new_path = 'mediafiles/' + project.code 
                save_path = settings.MEDIA_ROOT + '/' +  project.code  + '/' + _file.name
                path = default_storage.save(save_path, _file)
                
                name_file = path.split('/')[-1]
                f = File(file = project.code+ '/' + name_file,
                         name_file = name_file,
                         document = d)
                f.save()
                
                for m in metadata:
                    if 'file_'+str(i)+'_m_'+str(m.id) in request.POST:
                        f_m_r = File_Metadata_Relation(metadata = m,
                                                       file = f,
                                                       data_value = request.POST['file_'+str(i)+'_m_'+str(m.id)])
                    else:
                        f_m_r = File_Metadata_Relation(metadata = m,
                                                       file = f)
                    f_m_r.save()
                i+=1
    
            return HttpResponseRedirect(reverse_lazy('dashboard')+'?q='+project.name_project)
        
    else:
        return redirect('login')
    
    contexto = {'project':project, 'metadata': metadata, 'error': error, 'lenguas':lengua}
    return render(request, 'upload_document_form.html', contexto)


def lenguas():
    lengua = [["Aguacateco","AGU"], ["Akateko","KNJ"], ["Amuzgo","AZG"], ["Alemán", "DE"], ["Ayapaneco","AYA"], ["Ch'ol","CHL"], ["Chatino","CHAT"],
              ["Chichimeco","PEI"], ["Chinanteco","CHIN"], ["Chocholteco","COZ"], ["Chontal de la sierra de oaxaca","CHD"],
              ["Chontal de tabasco","CHF"], ["Chuj","CAC"], ["Cora","CRN"], ["Cucapá","COC"], ["Cuicateco","CUT"],
              ["Español","ES"], ["Francés", "FR"], ["Huarijio","VAR"], ["Huasteco","HUS"], ["Huave","HUV"], ["Huichol", "HCH"], ["Inglés","EN"],
              ["Italiano", "IT"], ["Ixcateco","IXC"], ["Ixil","IXL"], ["Jacalteco","JAC"], ["Kaqchikel","CAK"], ["Kikapú","KIC"], 
              ["Kiliwa","KLB"], ["Ku' ahl","PPI"],["Kumiai","DIH"], ["Lacandón","LAC"], ["Mam","MAM"], ["Maya","MY"], ["Mayo","MFY"], 
              ["Mazahua","MAZA"], ["Mazateco","MAZ"], ["Mixe","MXE"], ["Mixteco","MX"], ["Náhuatl","NAH"], ["Noruego", "NOR"],
              ["Oluteco","PLO"], ["Otomí", "OT"], ["Paipai","PAPAI"], ["Pápago","OOD"], ["Pima del norte","PIA"], ["Popoloca","POP"],
              ["Popoluca","PPA"], ["Portugués", "PT"], ["Purépecha","TSZ"], ["Q'anjob'al","KJB"], ["Qato'k","MHC"], ["Quekchí","KEK"], 
              ["Quiché","QUC"],["Ruso", "RU"], ["Sayulteco","POS"], ["Seri","SEI"], ["Tarahumara","TAC"], ["Teko","TTC"], 
              ["Tepehua","TPA"], ["Tepehuán","TPN"], ["Texistepequeño","POQ"], ["Tlapaneco","TCF"], ["Tojolabal","TOJ"], 
              ["Totonaco","TOT"], ["Triqui","TRC"], ["Tseltal","TZH"] ,["Tzotzil","TZO"], ["Yaqui","YAQ"], ["Zapoteco","ZAP"],
              ["Zoque","ZOR"]]
    return lengua


def list_collaborators_project_view(request):
    pass


def add_collaborator_view(request, id_project):
    project = Project.objects.get(id=id_project)
    colaboradores = project.project_members.all()
    error = ''
    email = ''
    sbj = '¡GECO te saluda!'
    msg = 'Hola, {0} {1} te invita a que te registres en GECO para colaborar en el proyecto {2}.\n\nPor favor utiliza este correo para tu registro en la siguiente dirección: http://172.16.199.134/accounts/register/\n\nEn caso de que quieras utilizar otro correo para registrarte, avísale a {0} por medio de su correo: {3}'.format(request.user.first_name, request.user.last_name, project.name_project, project.get_owner())

    if request.user.is_authenticated and project.get_owner()==request.user:
        if request.method == 'GET' and request.GET.get('q',False):
            id_colaborador = int(request.GET.get('q', ''))
            project.project_members.remove(id_colaborador)
            colaboradores = project.project_members.all()
            
        elif request.method == 'POST':
            email = request.POST['email_user']
            try:
                user = User.objects.get(email = email)
                project.project_members.add(user)
            except:
                error = "Usuario no encontrado. Ya se le ha enviado un correo electrónico invitándolo a que se registre"
                send_mail(sbj, msg, settings.DEFAULT_FROM_EMAIL, [email])
    else:
        return redirect('login')
    
    contexto = {'project':project, 'colaboradores':colaboradores, 'error': error, 'email': email}
    return render(request, 'add_collaborator_form.html', contexto)


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
            except:
                error = 'Hubo un error al enviar invitación al usuario'
    else:
        return redirect('login')
    
    contexto = {'error': error, 'email': email}
    return render(request, 'invite_user_form.html', contexto)


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


def download_project(request, project_id):
    project = Project.objects.get(id=project_id)

    currentDT = datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
    zipfile_name = "%s.zip" % currentDT
    currentDT = currentDT + '/' + project.code
    
    response = HttpResponse(content_type='application/zip')
    zip_file = zipfile.ZipFile(response, 'w')
    paths = glob(settings.MEDIA_ROOT + '/' + project.code + '/*.txt')

    for file in paths:
        fdir, fname = os.path.split(file)
        zip_path = os.path.join(currentDT, fname)
        zip_file.write(file, zip_path)
    response['Content-Disposition'] = 'attachment; filename={}'.format(zipfile_name)
    zip_file.close()

    return response


def download_document(request, document_id):
    document = Document.objects.get(id = document_id)
    files = File.objects.filter(document_id = document.id)
        
    currentDT = datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
    zipfile_name = "%s.zip" % currentDT
    
    response = HttpResponse(content_type='application/zip')
    zip_file = zipfile.ZipFile(response, 'w')
    
    for f in files:
        fdir, fname = os.path.split(f.file.path)
        zip_path = os.path.join(currentDT, fname)
        zip_file.write(f.file.path, zip_path)
    response['Content-Disposition'] = 'attachment; filename={}'.format(zipfile_name)
    zip_file.close()
    return response