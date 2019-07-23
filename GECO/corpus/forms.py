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
	files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
 
class contact_form(forms.Form):
	name = forms.CharField(label='Su nombre*', max_length=50)
	email = forms.EmailField(label='Su e-mail*')
	message = forms.CharField(label='Su pregunta*', widget=forms.Textarea(attrs={'rows': '10','cols': '50', 
                                                                              'placeholder': 'Escriba aquí su pregunta...'}))