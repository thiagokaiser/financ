from django import forms
from django.forms.widgets import TextInput
from .models import Transacao, Tag

class TransacaoFormView(forms.ModelForm):    
    class Meta:
        model = Transacao
        fields = ('valor',
				  'descricao',	
				  'dt_vencimento',
				  'tag',			
				  'pago',		
        		)
        widgets = {
            'dt_vencimento': TextInput(attrs={'type': 'date'}),
        }

class TagFormView(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('descricao',	
				  'cor',
        		)
        widgets = {
            'cor': TextInput(attrs={'type': 'color'}),
        }