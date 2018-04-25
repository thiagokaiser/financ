from django import forms
from django.forms.widgets import TextInput
from .models import Ponto

class PontoForm(forms.ModelForm):    
    class Meta:
        model = Ponto
        fields = ('dia',        
				  'hora',       
				  'observacao', 	
				  'tipo'       
        		)
        widgets = {
            'dia': TextInput(attrs={'type': 'date'}),
            'hora': TextInput(attrs={'type': 'time'}),
        }