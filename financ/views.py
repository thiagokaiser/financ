from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import (
	Despesa,
	Categoria,
	)
from .forms import (
	DespesaFormView,
	CategoriaFormView,
	)
from django.utils import timezone
from django.contrib import messages
from django.core import serializers
import datetime
import calendar
import json

# Create your views here.
def Despesas(request):
	p_ano    = int(request.GET.get('year', datetime.datetime.today().year))
	p_mes    = int(request.GET.get('month', datetime.datetime.today().month))	
	current = datetime.datetime(p_ano, p_mes, 1)
	if (current.month - 1) == 0:
		current = datetime.datetime(p_ano , p_mes, 1)
		next_month = datetime.datetime(p_ano, 2, 1)
		prev_month = datetime.datetime((current.year - 1), 12, 1)
	elif (current.month + 1) == 13:
		next_month = datetime.datetime((current.year + 1), 1, 1)
		prev_month = datetime.datetime(current.year, 11, 1)
	else:
		next_month = datetime.datetime(current.year, (current.month + 1), 1)
		prev_month = datetime.datetime(current.year, (current.month - 1), 1)
	mes = dict()
	mes['atual']        = current	
	mes['proximo']  	= next_month
	mes['anterior'] 	= prev_month	

	despesas = Despesa.objects.filter(dt_vencimento__year=current.year,
                                          dt_vencimento__month=current.month)

	args = {'mes': mes,
	 		'despesas': despesas}

	return render(request, 'financ/despesas.html', args)

def Despesa_Add(request):
	if request.method == 'POST':
		form = DespesaFormView(request.POST)
		if form.is_valid():  
			despesa = form.save(commit=False)           	
			url = '?year=' + str(despesa.dt_vencimento.year) + '&month=' + str(despesa.dt_vencimento.month)
			despesa.save()            
			messages.success(request, "Informações atualizadas com sucesso.", extra_tags='alert-success alert-dismissible')
			response = redirect('financ:despesas')

			response['Location'] += url
			return response
		else:
			messages.error(request, "Foram preenchidos dados incorretamente.", extra_tags='alert-error alert-dismissible')               
	else:
		form = DespesaFormView()

	args = {'form': form, 'form_categ': CategoriaFormView()}

	return render(request, 'financ/despesa_add.html', args)

def Despesa_View(request,pk):
    despesa = get_object_or_404(Despesa, pk=pk)
    
    args = {'despesa': despesa}

    return render(request, 'financ/despesa_view.html', args)

def Despesa_Edit(request,pk):
	despesa = get_object_or_404(Despesa, pk=pk)
	if request.method == 'POST':
		form = DespesaFormView(request.POST, instance=despesa)        
		if form.is_valid():  
			despesa = form.save(commit=False)           	
			url = '?year=' + str(despesa.dt_vencimento.year) + '&month=' + str(despesa.dt_vencimento.month)
			despesa.save()            
			messages.success(request, "Informações atualizadas com sucesso.", extra_tags='alert-success alert-dismissible')
			response = redirect('financ:despesas')

			response['Location'] += url
			return response
		else:
			messages.error(request, "Foram preenchidos dados incorretamente.", extra_tags='alert-error alert-dismissible')               
	else:
		form = DespesaFormView(instance=despesa)        

	args = {'form': form}    

	return render(request, 'financ/despesa_edit.html', args)

def Categoria_Add(request):
	if request.is_ajax():
		if request.method == 'POST':
			form = CategoriaFormView(request.POST)
			if form.is_valid():
				salvar = form.save()			
				retorno_dict = {'chave': salvar.pk, 'descricao': salvar.descricao}				
			else:
				retorno_dict = {'chave': 'erro', 'descricao': str(form.errors)}

			retorno = json.dumps(retorno_dict)
			return HttpResponse(retorno)
		
	else:	
		if request.method == 'POST':
			form = CategoriaFormView(request.POST)
			if form.is_valid():
				form.save()
				return redirect('financ:categoria_list')
		else:
			form = CategoriaFormView()

		args = {'form': form}

		return render(request, 'financ/categoria_add.html', args)

def Categoria_List(request):	
	categorias = Categoria.objects.all()
	args = {'categorias': categorias}
	return render(request, 'financ/categoria_list.html', args)

def Categoria_View(request, pk):
	categoria = get_object_or_404(Categoria, pk=pk)

	args = {'categoria': categoria}
	return render(request, 'financ/categoria_view.html', args)

def Categoria_Edit(request, pk):
	categoria = get_object_or_404(Categoria, pk=pk)
	if request.method == 'POST':
		form = CategoriaFormView(request.POST, instance=categoria)        
		if form.is_valid():  			
			form.save()            
			messages.success(request, "Informações atualizadas com sucesso.", extra_tags='alert-success alert-dismissible')
			
			return redirect('financ:categoria_list')
		else:
			messages.error(request, "Foram preenchidos dados incorretamente.", extra_tags='alert-error alert-dismissible')               
	else:
		form = CategoriaFormView(instance=categoria)        

	args = {'form': form}    

	return render(request, 'financ/despesa_edit.html', args)

def Categoria_Del(request):
    if request.POST and request.is_ajax():        
        if request.POST.getlist('categoria_lista[]'):
            categoria_list = request.POST.getlist('categoria_lista[]')            
            for i in categoria_list:
                categoria = Categoria.objects.get(pk=i)
                categoria.delete()            
            messages.success(request, "Mensagens excluidas com sucesso.", extra_tags='alert-success alert-dismissible')            
        else:
            messages.error(request, "Nenhuma mensagem selecionada.", extra_tags='alert-error alert-dismissible')               

    return HttpResponse('')
