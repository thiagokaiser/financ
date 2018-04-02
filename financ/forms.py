from django import forms
from django.forms.widgets import TextInput
from .models import Despesa, Categoria

class DespesaFormView(forms.ModelForm):    
    class Meta:
        model = Despesa
        fields = ('valor',
				  'descricao',	
				  'dt_vencimento',
				  'categoria',			
				  'pago',		
        		)
        widgets = {
            'dt_vencimento': TextInput(attrs={'type': 'date'}),
        }

class CategoriaFormView(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ('descricao',	
				  'cor',
        		)
        widgets = {
            'cor': TextInput(attrs={'type': 'color'}),
        }