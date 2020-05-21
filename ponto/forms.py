from django import forms
from django.forms.widgets import TextInput
from .models import Ponto, ParamPonto

class PontoForm(forms.ModelForm):    
	class Meta:
		model = Ponto
		fields = ('dia',
				  'hora',       
				  'observacao', 	
				  'tipo',
				  'comprovante'
				)
		widgets = {
			'dia': TextInput(attrs={'type': 'date'}),
			'hora': TextInput(attrs={'type': 'time'}),
		}

class PontoFormView(forms.ModelForm):        
	class Meta:
		model = Ponto
		fields = ('dia',
				  'hora',
				  'observacao',
				  'tipo',
				)
		widgets = {
			'dia': TextInput(attrs={'type': 'date', 'disabled': True}),
			'hora': TextInput(attrs={'type': 'time', 'disabled': True}),
			'observacao': TextInput(attrs={'disabled': True}),
			'tipo': TextInput(attrs={'disabled': True}),
		}

class ParamPontoForm(forms.ModelForm):    
	class Meta:
		model = ParamPonto
		fields = ('entrada',
				  'saida',
				  'tolerancia'

				)
		widgets = {
			'entrada': TextInput(attrs={'type': 'time'}),
			'saida': TextInput(attrs={'type': 'time'}),
			'tolerancia': TextInput(attrs={'type': 'time'}),
		}