from django import forms
from django.forms.widgets import CheckboxSelectMultiple

from .models import *

class create_project_form(forms.ModelForm):

    name_project = forms.CharField(label='Nombre del proyecto', max_length=100, widget=forms.TextInput(attrs={'style':'width:100%;'}))
    description = forms.CharField(label='Descripción del proyecto', max_length=250, widget=forms.Textarea(attrs={'placeholder': 'Escriba aquí la descripción del proyecto...', 'rows':'3', 'style':'width:100%;'}))
    public_status = forms.BooleanField(label='¿Será público?', required=False, initial=False, widget="")
    collab_status = forms.BooleanField(label='¿Será colaborativo?', required=False, initial=False)
    parallel_status = forms.BooleanField(label='¿Será para corpus paralelo?', required=False, initial=False)
    
    class Meta:
        model = Project
        fields = [
            'name_project',
            'description',
            'public_status',
            'collab_status',
            'parallel_status',
        ]
        


class metadata_project_form(forms.ModelForm):
    
    name_metadata = forms.MultipleChoiceField(
        label='Metadatos para su proyecto',
        widget= CheckboxSelectMultiple(),
        choices=(
            (1, "Lengua"),
            (2, "Título"),
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
            ),
        required=True
    )
    
    class Meta:
        model = Metadata
        fields = ('name_metadata',)


class add_collaborator_form(forms.Form):
    project_name = forms.CharField(max_length=100)
    project_member = forms.CharField(label='Usuario', max_length=100)

class document_form(forms.Form):
    project_name = forms.CharField(max_length=100)
    files = forms.FileField(label="Selecciona los archivos", widget=forms.ClearableFileInput(attrs={'multiple': True}))
 
class contact_form(forms.Form):
    name = forms.CharField(label='Su nombre*', max_length=50)
    email = forms.EmailField(label='Su e-mail*')
    message = forms.CharField(label='Su pregunta*', widget=forms.Textarea(attrs={'placeholder': 'Escriba aquí su pregunta...'}))

class data_document_form(forms.Form):
    project_name = forms.CharField(max_length=100)

    def __init__(self, *args,**kwargs):
        self.choices_doc = kwargs.pop('choices_doc')
        self.choices_md = kwargs.pop('choices_md')
        super(data_document_form, self).__init__(*args, **kwargs)
        self.fields['document'] = forms.ChoiceField(choices=self.choices_doc)  
        self.fields['metadata'] = forms.ChoiceField(choices=self.choices_md)
    
    data = forms.CharField(max_length=100)