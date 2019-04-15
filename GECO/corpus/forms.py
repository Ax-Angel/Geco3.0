from django import forms

class normal_project_form(forms.Form):
	name = forms.CharField(label='Nombre del proyecto', max_length=100)
	is_public = forms.BooleanField(required=False, initial=False)
	is_collab = forms.BooleanField(required=False, initial=False)