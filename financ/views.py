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
from .despesa import (
	AlteraDespesasPend,
	BuscaDespesasMes,
	EliminaDespesa,
	EditaDespesa,
	AdicionaDespesa,
	GeraExcel
	)
import datetime
import calendar
import json
#import time

#import pdb; pdb.set_trace()

# Create your views here.
def Despesas(request):
	p_ano    = int(request.GET.get('year', datetime.datetime.today().year))
	p_mes    = int(request.GET.get('month', datetime.datetime.today().month))	

	try:
		current = datetime.datetime(p_ano, p_mes, 1)
	except:
		messages.error(request, "Foram preenchidos dados incorretamente.", extra_tags='alert-error alert-dismissible')               
		return redirect('financ:despesas')

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
	mes['ultdia']       = next_month - datetime.timedelta(days=1)

	despesas, totais = BuscaDespesasMes(request,current.year,current.month)

	args = {'mes': mes,
	 		'despesas': despesas,
	 		'totais': totais}

	return render(request, 'financ/despesas.html', args)

def Despesa_Add(request):	
	p_ano    = int(request.GET.get('year', datetime.datetime.today().year))
	p_mes    = int(request.GET.get('month', datetime.datetime.today().month))	
	current  = datetime.datetime(p_ano , p_mes, 1)
	mes = dict()
	mes['atual'] = current

	if request.method == 'POST':
		p_fixa    = bool(request.POST.get('id_repetir'))
		
		p_qtd_meses = request.POST.get('id_meses')
		if p_qtd_meses != '':
			qtd_meses = int(p_qtd_meses)
			if qtd_meses > 99:
				qtd_meses = 99
		else:
			qtd_meses = 2		

		form = DespesaFormView(request.POST, user=request.user)

		if form.is_valid():  
			despesa = form.save(commit=False)           	
			url = '?year=' + str(despesa.dt_vencimento.year) + '&month=' + str(despesa.dt_vencimento.month)
			despesa.fixa = p_fixa
			despesa.usuario = request.user						
			if despesa.fixa == True:				
				despesa.parcela = '1/' + str(qtd_meses)
			despesa.save()       			   
			if despesa.fixa == True:
				AdicionaDespesa(despesa,qtd_meses)  
				
			messages.success(request, "Informações atualizadas com sucesso.", extra_tags='alert-success alert-dismissible')
			response = redirect('financ:despesas')

			response['Location'] += url
			return response
		else:
			messages.error(request, "Foram preenchidos dados incorretamente.", extra_tags='alert-error alert-dismissible')               		
	else:
		form = DespesaFormView(user=request.user)

	args = {'form': form, 'form_categ': CategoriaFormView(), 'mes': mes}

	return render(request, 'financ/despesa_add.html', args)

def Despesa_View(request,pk):
	p_ano    = int(request.GET.get('year', datetime.datetime.today().year))
	p_mes    = int(request.GET.get('month', datetime.datetime.today().month))	
	current  = datetime.datetime(p_ano , p_mes, 1)
	mes = dict()
	mes['atual'] = current

	despesa = get_object_or_404(Despesa, pk=pk)
	if despesa.usuario != request.user:
		messages.error(request, "Acesso negado!", extra_tags='alert-error alert-dismissible')			
		return redirect('financ:despesas')    
	despesa.dt_vencimento = datetime.date(p_ano,p_mes,despesa.dt_vencimento.day)

	args = {'despesa': despesa,
			'mes': mes,}

	return render(request, 'financ/despesa_view.html', args)

def Despesa_Edit(request,pk):
	p_ano    = int(request.GET.get('year', datetime.datetime.today().year))
	p_mes    = int(request.GET.get('month', datetime.datetime.today().month))	
	p_fixa   = int(request.GET.get('fixa', 0))	
	url      = '?year=' + str(p_ano) + '&month=' + str(p_mes)

	despesa = get_object_or_404(Despesa, pk=pk)
	if despesa.usuario != request.user:
		messages.error(request, "Acesso negado!", extra_tags='alert-error alert-dismissible')			
		return redirect('financ:despesas')

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
		data = {}		
		form = DespesaFormView(instance=despesa,
							   initial=data,
							   user=request.user)       		

	args = {'form': form, 'despesa': despesa, 'param': ''}    
	return render(request, 'financ/despesa_edit.html', args)

def Despesa_Edit_All(request,pk):
	p_ano    = int(request.GET.get('year', datetime.datetime.today().year))
	p_mes    = int(request.GET.get('month', datetime.datetime.today().month))	
	p_fixa   = int(request.GET.get('fixa', 0))	
	url      = '?year=' + str(p_ano) + '&month=' + str(p_mes)

	despesa = get_object_or_404(Despesa, pk=pk)
	if despesa.usuario != request.user:
		messages.error(request, "Acesso negado!", extra_tags='alert-error alert-dismissible')			
		return redirect('financ:despesas')

	if request.method == 'POST':
		form = DespesaFormView(request.POST, instance=despesa)        
		if form.is_valid():  
			despesa = form.save(commit=False)           	
			url = '?year=' + str(despesa.dt_vencimento.year) + '&month=' + str(despesa.dt_vencimento.month)
			despesa.save()

			AlteraDespesasPend(despesa)

			messages.success(request, "Informações atualizadas com sucesso.", extra_tags='alert-success alert-dismissible')
			response = redirect('financ:despesas')

			response['Location'] += url
			return response
		else:
			messages.error(request, "Foram preenchidos dados incorretamente.", extra_tags='alert-error alert-dismissible')               
	else:				
		data = {}		
		form = DespesaFormView(instance=despesa,
							   initial=data,
							   user=request.user)       		

	args = {'form': form, 'despesa': despesa, 'param': 'all'}    
	return render(request, 'financ/despesa_edit.html', args)

def Despesa_Del(request):
	p_ano    = int(request.GET.get('year', datetime.datetime.today().year))
	p_mes    = int(request.GET.get('month', datetime.datetime.today().month))	
	p_fixa   = int(request.GET.get('fixa', 0))	

	url = '?year=' + str(p_ano) + '&month=' + str(p_mes)
	
	EliminaDespesa(request,1)            

	return HttpResponse('')	

def Despesa_Del_All(request):
	p_ano    = int(request.GET.get('year', datetime.datetime.today().year))
	p_mes    = int(request.GET.get('month', datetime.datetime.today().month))	
	p_fixa   = int(request.GET.get('fixa', 0))	

	url = '?year=' + str(p_ano) + '&month=' + str(p_mes)

	EliminaDespesa(request,2)
	
	return HttpResponse('')	

def Categoria_Add(request):
	if request.is_ajax():
		if request.method == 'POST':
			form = CategoriaFormView(request.POST)
			if form.is_valid():
				categoria = form.save(commit=False)           	
				categoria.usuario = request.user
				categoria.save()
				retorno_dict = {'chave': categoria.pk, 'descricao': categoria.descricao}				
			else:
				retorno_dict = {'chave': 'erro', 'descricao': str(form.errors)}

			retorno = json.dumps(retorno_dict)
			return HttpResponse(retorno)
		
	else:	
		if request.method == 'POST':
			form = CategoriaFormView(request.POST)
			if form.is_valid():
				categoria = form.save(commit=False)           	
				categoria.usuario = request.user
				categoria.save()
				return redirect('financ:categoria_list')
		else:
			form = CategoriaFormView()

		args = {'form': form}

		return render(request, 'financ/categoria_add.html', args)

def Categoria_List(request):	
	categorias = Categoria.objects.filter(usuario=request.user)	
	args = {'categorias': categorias}
	return render(request, 'financ/categoria_list.html', args)

def Categoria_View(request, pk):
	categoria = get_object_or_404(Categoria, pk=pk)
	if categoria.usuario != request.user:
		messages.error(request, "Acesso negado!", extra_tags='alert-error alert-dismissible')			
		return redirect('financ:categoria_list')

	args = {'categoria': categoria}
	return render(request, 'financ/categoria_view.html', args)

def Categoria_Edit(request, pk):
	categoria = get_object_or_404(Categoria, pk=pk)
	if categoria.usuario != request.user:
		messages.error(request, "Acesso negado!", extra_tags='alert-error alert-dismissible')			
		return redirect('financ:categoria_list')
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

	return render(request, 'financ/categoria_edit.html', args)

def Categoria_Del(request):
    if request.POST and request.is_ajax():        
        if request.POST.getlist('categoria_lista[]'):
            categoria_list = request.POST.getlist('categoria_lista[]')            
            for i in categoria_list:
                categoria = Categoria.objects.get(pk=i)
                if categoria.usuario != request.user:
                    messages.error(request, "Acesso negado!", extra_tags='alert-error alert-dismissible')			
                    return redirect('financ:categoria_list')
                categoria.delete()            
            messages.success(request, "Mensagens excluidas com sucesso.", extra_tags='alert-success alert-dismissible')            
        else:
            messages.error(request, "Nenhuma mensagem selecionada.", extra_tags='alert-error alert-dismissible')               

    return HttpResponse('')

def Gera_XLS_Mes(request):
	p_data_ini    = request.GET.get('data_ini')
	p_data_fim    = request.GET.get('data_fim')

	try:		
		data_ini = datetime.datetime(int(p_data_ini[:4]), int(p_data_ini[5:7]), int(p_data_ini[8:10]))
		data_fim = datetime.datetime(int(p_data_fim[:4]), int(p_data_fim[5:7]), int(p_data_fim[8:10]))
	except:
		messages.error(request, "Data inválida.", extra_tags='alert-error alert-dismissible')    
		return redirect('financ:despesas')	

	despesas = Despesa.objects.filter(dt_vencimento__gte=data_ini,
                                      dt_vencimento__lte=data_fim,
                                      usuario=request.user)

	#time.sleep(3)

	response = HttpResponse(content_type='application/vnd.ms-excel')
	#response['Set-Cookie'] = "fileDownload=true; path=/"
	response['Content-Disposition'] = 'attachment; filename=despesas' + str(data_ini.date()) + "to" + str(data_fim.date()) + '.xlsx'

	xlsx_data = GeraExcel(despesas)
	response.write(xlsx_data)
	return response
