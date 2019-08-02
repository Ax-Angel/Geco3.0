from django import forms
from .models import *

class create_project_form(forms.Form):
    name = forms.CharField(label='Nombre del proyecto', max_length=100)
    is_public = forms.BooleanField(required=False, initial=False)
    is_collab = forms.BooleanField(required=False, initial=False)
    is_parallel = forms.BooleanField(required=False, initial=False)

class add_collaborator_form(forms.Form):
    project_name = forms.CharField(max_length=100)
    project_member = forms.CharField(label='Usuario', max_length=100)

class document_form(forms.Form):
    project_name = forms.CharField(max_length=100)
    files = forms.FileField(label="Selecciona los archivos", widget=forms.ClearableFileInput(attrs={'multiple': True}))
 
class contact_form(forms.Form):
    name = forms.CharField(label='Su nombre*', max_length=50)
    email = forms.EmailField(label='Su e-mail*')
    message = forms.CharField(label='Su pregunta*', widget=forms.Textarea(attrs={'rows': '10','cols': '50', 
                                                                              'placeholder': 'Escriba aquí su pregunta...'}))
METADATA = (
    (1, "Lengua"),
    (2, "Titulo"),
    (3, "Autor"),
    (4, "Editorial"),
    (5, "Variante en el texto"),
    (6, "Variantes de la lengua en norma ISO"),
    (7, "Año"),
    (8, "País"),
    (9, "Estado"),
    (10, "División regional"),
    (11, "Comunidad a la que pertenece"),
    (12, "Clasificación genérica"),
    (13, "Notas"),
)

class metadata_project_form(forms.Form):
    metadata_list = forms.MultipleChoiceField(
            choices=METADATA, 
            label="...",
            widget=forms.CheckboxSelectMultiple(), 
            required=True)
    project_name = forms.CharField(max_length=100)


class data_document_form(forms.Form):
    project_name = forms.CharField(max_length=100)

    def __init__(self, *args,**kwargs):
        self.choices_doc = kwargs.pop('choices_doc')
        self.choices_md = kwargs.pop('choices_md')
        super(data_document_form, self).__init__(*args, **kwargs)
        self.fields['document'] = forms.ChoiceField(choices=self.choices_doc)  
        self.fields['metadata'] = forms.ChoiceField(choices=self.choices_md)
    
    data = forms.CharField(max_length=100)