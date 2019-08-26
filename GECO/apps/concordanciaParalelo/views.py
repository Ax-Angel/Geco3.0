import traceback
import csv
import datetime
import xlwt
import re

from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponseBadRequest, HttpResponse

from corpus.models import *
from users.models import User
from apps.concordanciaParalelo.function import *

#Show interface for the parallel corpus concordance
def concordance_paralle_view(request):
    project_select = None
    languages = []
    lang_select = ''
    style_display = 'none'
    search_petition = ''
    positional_annotation = [['palabra', 'checked', '']]
    #positional_annotation = [['palabra', 'checked', ''], ['lemma', '', ''], ['POS', '', '']]
    alignment = []
    alignment_select = []
    max_view = '-'
    visualize = 0
    window = request.session.get('window', 'Vertical')
    filter_metadato = []
    filter_select = {}
    results = request.session.get('results')
    results = []
    project = []
    project_public = []
    
    all_projects = Project.objects.filter(parallel_status = True)
    if request.user.is_authenticated:
        for proj in all_projects:
            if proj.is_user_collaborator(request.user):
                project.append(proj)
            elif proj.is_public():
                project_public.append(proj)
    else:
        project = []
        project_public = Project.objects.filter(parallel_status = True).filter(public_status = True) 
    
    metadata_idioma = Metadata.objects.get(name_metadata='Lengua')

    if request.method == 'GET':
        project_select = None
        if request.GET.get('q',False):
            #'q' in request.GET
            query_string = request.GET.get('q')
            query_list = query_string.split('/')
            
            if len(query_list) == 0:
                return HttpResponseBadRequest('Invalid Search')
            
            #In case that select it one project
            #format of send -> ?q={{project.id}}
            if len(query_list) >=1:
                style_display = 'none'
                project_select = Project.objects.get(id=int(query_list[0]))
                dct = {'project_select':project_select, 'metadata_idioma':metadata_idioma}
                if Document.objects.filter(project_id=dct['project_select'].id).exists():
                    docs = Document.objects.filter(project_id=dct['project_select'].id)
                    dct.update({'docs':docs})
                else:
                    dct.update({'docs':[]})
                languages = type_search_languages(dct)
                
            #In case that select it one search language
            #format of send -> ?q={{project.id}}/{{lang_select}}
            if len(query_list) >= 2:
                style_display = '' 
                lang_select = query_list[1]
                dct.update({'lang_select':lang_select})
                #positional_annotation = type_positicional_annotation(dct)                    
                alignment = type_alignment(dct)
                project_metadato = Metadata.objects.filter(project=dct['project_select'])
                dct.update({'project_metadato':project_metadato})
                filter_metadato = filter_metadata(dct)['filter_metadato']
                               
    #Sending search request for concordance
    elif request.method == 'POST':
        style_display = ''
        project_select = Project.objects.get(id=int(request.POST['id_project']))
        lang_select = request.POST['lang_select']
        docs = Document.objects.filter(project_id=project_select.id)
        project_metadato = Metadata.objects.filter(project=project_select)
        dct = {'project_select':project_select,'metadata_idioma':metadata_idioma, 'docs':docs,
                'lang_select':lang_select, 'project_metadato':project_metadato}
        
        languages = type_search_languages(dct)
        alignment = type_alignment(dct)
        alignment_select = request.POST.getlist('alignment')        
        positional = request.POST.getlist('positional')
        dct.update({'positional':positional})
        #positional_annotation = type_positicional_annotation(dct)
        max_view = request.POST['max_view']
        search_petition = request.POST['search_petition']
        window = request.POST['window']
        dct.update({'alignment':alignment})
        dct.update({'alignment_select':alignment_select})
        
        r_f = filter_metadata(dct)
        filter_metadato = r_f['filter_metadato']
        id_metadato_filter_project_select = r_f['id_metadato']
        if id_metadato_filter_project_select:
            for i in id_metadato_filter_project_select:
                if str(i) in request.POST.keys() and request.POST[str(i)] and request.POST[str(i)]!='Seleccione...':
                    filter_select.update({str(i): request.POST[str(i)]})
        dct.update({'filter_select':filter_select})
        dicc_file = find_files(dct)
        _file = dicc_file['_file']
        files_corpus = dicc_file['files_corpus']
        
        dicc_search = type_search(search_petition)
        
        if bool(dicc_search):
            for i,path in enumerate(_file):
                pathes = files_corpus[i]
                dicc_search.update({'language':lang_select})
                results = search_request(path, pathes, alignment_select.copy(), dicc_search, window, results)
        else:
            results = []
            
        if max_view=='-':
            visualize = len(results)
        else:
            if window == 'Vertical':
                visualize = int(max_view)+1
            else:
                visualize = int(max_view)
        
    request.session['window'] = window    
    request.session['results'] = results
    
    contexto = {'project':project, 'project_public':project_public, 'languages':languages,
                'project_select':project_select, 'style_display':style_display, 'lang_select':lang_select,
                'positional_annotation':positional_annotation, 'alignment':alignment, 'visualize':visualize,
                'alignment_select':alignment_select, 'max_view':max_view, 'window':window, 'filter_metadato':filter_metadato,
                'filter_select':filter_select, 'search_petition':search_petition, 'results':results}
    
    return render(request, 'concordance_paralle_form.html', contexto)

#Type of positional annotation
def type_positicional_annotation(dct):
    if dct['lang_select'] in ['ES', 'EN', 'FR', 'IT']:
        positional_annotation = [['palabra', 'checked', ''], ['lemma', '', ''], ['POS', '', '']]
    elif dct['lang_select'] in ['NH', 'MX', 'OT', 'MY', 'CTU', 'AZG', 'MZ', 'CA', 'EO']:
        positional_annotation = [['palabra', 'checked', ''], ['lemma', '', 'none'], ['POS', '', 'none']]
    elif dct['lang_select'] in ['DE']:
        positional_annotation = [['palabra', 'checked', ''], ['lemma', '', ''], ['POS', '', 'none']]
    else:
        positional_annotation = [['palabra', 'checked', ''], ['lemma', '', 'none'], ['POS', '', 'none']]
    
    if 'positional' in dct.keys():
        for p in positional_annotation:
            if p[0] in dct['positional']:
                p[1]='checked'
            else:
                p[1]=''
    return positional_annotation

#Type of search languages
def type_search_languages(dct):
    languages = set()
    for d in dct['docs']:
        files = File.objects.filter(document_id=d.id)
        for f in files: 
            data = File_Metadata_Relation.objects.filter(metadata_id=dct['metadata_idioma'].id, file_id=f.id)
            if data.exists():
                languages.add(data[0].data_value)
    languages = list(languages)
    return languages

#Type of alignment
def type_alignment(dct):
    alignment = set()
    for d in dct['docs']:
        files = File.objects.filter(document_id=d.id)
        lang = set()
        for f in files:
            data = File_Metadata_Relation.objects.filter(metadata_id=dct['metadata_idioma'].id, file_id=f.id)
            if data.exists():
                lang.add(data[0].data_value)
        if len(lang)!=0 and dct['lang_select'] in lang:
            lang.discard(dct['lang_select'])
            alignment.update(lang)
    alignment = list(alignment)
    return alignment

#Find the file types for the concordance
def find_files(dct):
    _file = []
    files_corpus = []
                
    for d in dct['docs']:
        files = File.objects.filter(document_id=d.id)
        tuple_file = ()
        array_files = []
        for f in files:
            dato = File_Metadata_Relation.objects.filter(file_id=f.id)
            
            if dato.filter(metadata_id=dct['metadata_idioma'].id, data_value=dct['lang_select']).exists():
                if dct['filter_select']:
                    exist_file_filtro = False
                    for k,v in dct['filter_select'].items():
                        if dato.filter(metadata_id=int(k), data_value=v).exists():
                            exist_file_filtro = True
                        else:
                            exist_file_filtro = False
                    if exist_file_filtro:
                        tuple_file = (f.file.path, dct['lang_select'])
                else:
                    tuple_file = (f.file.path, dct['lang_select'])
            else:
                t_aux = ()
                dato = dato.filter(metadata_id=dct['metadata_idioma'].id)
                if dato[0].data_value in dct['alignment_select']:
                    t_aux = (f.file.path, dato[0].data_value)
                    array_files.append(t_aux)
        #if len(tuple_file)!=0 and len(array_files)==len(dct['alignment_select']):
        if len(tuple_file)!=0 and (dct['alignment_select']==[] or len(array_files)!=0):
            _file.append(tuple_file)
            files_corpus.append(array_files)

    return {'_file':_file, 'files_corpus':files_corpus}

#Show metadata values for filtering
def filter_metadata(dct):
    filter_metadato = []
    id_metadato =[]
    
    if dct['project_metadato'].exists():        
        for p_m in dct['project_metadato']:
            if p_m.id!=dct['metadata_idioma'].id:
                id_metadato.append(p_m.id)
                filter_metadato.append([p_m.id, p_m.name_metadata, set()])
        
        for d in dct['docs']:
            files = File.objects.filter(document_id=d.id)
            for f in files:
                dato_file = File_Metadata_Relation.objects.filter(file_id=f.id)
                if dato_file.filter(metadata_id=dct['metadata_idioma'].id, data_value=dct['lang_select']).exists():
                    for _d_f in dato_file:
                        if _d_f.metadata.id in id_metadato:
                            i = id_metadato.index(_d_f.metadata.id)
                            if _d_f.data_value != "":
                                filter_metadato[i][2].add(_d_f.data_value)
        j = 0
        k = len(filter_metadato)
        while j < k:
            if filter_metadato[j][2]:
                filter_metadato[j][2] = list(filter_metadato[j][2])
                j+=1
            else:
                del filter_metadato[j]
                k-=1
    return {'filter_metadato':filter_metadato, 'id_metadato':id_metadato}

def export_search_csv(request):
    currentDT = datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
    name_file = currentDT+".csv"
    response = HttpResponse(content_type='text/csv')  
    response['Content-Disposition'] = 'attachment; filename='+name_file 
    writer = csv.writer(response)
    response.write(u'\ufeff'.encode('utf8'))
    window = request.session.get('window')
    results = request.session.get('results')
    if window == 'Vertical':
        for r in results:
            r = re.sub(r'<strong>', '', r)
            r = re.sub(r'</strong>', '', r)
            writer.writerow(r)   
    elif window == 'Horizontal':
        for r in results:
            for x in r:
                x = re.sub(r'<strong>', '', x)
                x = re.sub(r'</strong>', '', x)
                writer.writerow(x)       
    elif window == 'KWIC':
        for r in results:
            for i,x in enumerate(r):
                if i==0:
                    writer.writerow([x[0], x[1][0], x[1][1], x[1][2]])
                else:
                    writer.writerow(x)
    return response  

def export_search_xls(request):
    currentDT = datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
    name_file = currentDT+".xls"
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename='+name_file 
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Concordancia')
    window = request.session.get('window')
    results = request.session.get('results')
    row = 0
    if window == 'Vertical':
        for res in results:
            for i,x in enumerate(res):
                x = re.sub(r'<strong>', '', x)
                x = re.sub(r'</strong>', '', x)
                ws.write(row, i, x)
            row += 1
    elif window == 'Horizontal':
        for res in results:
            for r in res:
                for i,x in enumerate(r):
                    x = re.sub(r'<strong>', '', x)
                    x = re.sub(r'</strong>', '', x)
                    ws.write(row, i, x)
                row += 1            
    elif window == 'KWIC':
        for res in results:
            for i,r in enumerate(res):
                if i==0:
                    for j,x in enumerate(r):
                        if j==0:
                            ws.write(row, j, x)
                        else:
                            for k,y in enumerate(x):
                                ws.write(row, k+1, y)
                else:
                    for j,x in enumerate(r):
                        ws.write(row, j, x)
                row += 1
    wb.save(response)
    return response

