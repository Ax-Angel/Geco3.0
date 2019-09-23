from django import template
from django.template.defaultfilters import register

from corpus.models import *
from apps.concordanciaParalelo.function import *

@register.filter(name='get_item')
def get_item(dictionary, index):
    if index in dictionary:
        return dictionary[index]
    return ''

@register.filter(name='a_sub_b')
def a_sub_b(a, b):
    return a-b

@register.filter(name='here')
def here(a):
    if a in [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]:
        return True
    return False

@register.filter(name='document_text')
def document_text(id_document):    
    document = Document.objects.get(id=id_document)
    files = File.objects.filter(document_id=document.id)
    textos = []
    for f in files:
        _tmp = []
        _tmp.append(f.id)
        _tmp.append(f.name_file)
        _tmp.append(read_text_txt(f.file.path))
        textos.append(_tmp)
    return textos