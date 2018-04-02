from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import (
	Transacao,
	Tag,
	)
from .forms import (
	TransacaoFormView,
	TagFormView,
	)
from django.utils import timezone
from django.contrib import messages
import datetime
import calendar

# Create your views here.
def Transacoes(request):
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

	transacoes = Transacao.objects.filter(dt_vencimento__year=current.year,
                                          dt_vencimento__month=current.month)

	args = {'mes': mes,
	 		'transacoes': transacoes}

	return render(request, 'transac/transac.html', args)

def Transacao_Add(request):
	if request.method == 'POST':
		form = TransacaoFormView(request.POST)
		if form.is_valid():  
			transacao = form.save(commit=False)           	
			url = '?year=' + str(transacao.dt_vencimento.year) + '&month=' + str(transacao.dt_vencimento.month)
			transacao.save()            
			messages.success(request, "Informações atualizadas com sucesso.", extra_tags='alert-success alert-dismissible')
			response = redirect('transac:transacoes')

			response['Location'] += url
			return response
		else:
			messages.error(request, "Foram preenchidos dados incorretamente.", extra_tags='alert-error alert-dismissible')               
	else:
		form = TransacaoFormView()

	args = {'form': form}

	return render(request, 'transac/transac_add.html', args)

def Transacao_View(request,pk):
    transacao = get_object_or_404(Transacao, pk=pk)
    
    args = {'transacao': transacao}

    return render(request, 'transac/transac_view.html', args)

def Transacao_Edit(request,pk):
	transacao = get_object_or_404(Transacao, pk=pk)
	if request.method == 'POST':
		form = TransacaoFormView(request.POST, instance=transacao)        
		if form.is_valid():  
			transacao = form.save(commit=False)           	
			url = '?year=' + str(transacao.dt_vencimento.year) + '&month=' + str(transacao.dt_vencimento.month)
			transacao.save()            
			messages.success(request, "Informações atualizadas com sucesso.", extra_tags='alert-success alert-dismissible')
			response = redirect('transac:transacoes')

			response['Location'] += url
			return response
		else:
			messages.error(request, "Foram preenchidos dados incorretamente.", extra_tags='alert-error alert-dismissible')               
	else:
		form = TransacaoFormView(instance=transacao)        

	args = {'form': form}    

	return render(request, 'transac/transac_edit.html', args)

def Tag_Add(request):
	if request.method == 'POST':
		form = TagFormView(request.POST)
		if form.is_valid():
			form.save()
			return redirect('transac:tag_list')
	else:
		form = TagFormView()

	args = {'form': form}

	return render(request, 'transac/tag_add.html', args)

def Tag_List(request):	
	tags = Tag.objects.all()
	args = {'tags': tags}
	return render(request, 'transac/tag_list.html', args)

def Tag_View(request, pk):
	tag = get_object_or_404(Tag, pk=pk)

	args = {'tag': tag}
	return render(request, 'transac/tag_view.html', args)

def Tag_Edit(request, pk):
	tag = get_object_or_404(Tag, pk=pk)
	if request.method == 'POST':
		form = TagFormView(request.POST, instance=tag)        
		if form.is_valid():  			
			form.save()            
			messages.success(request, "Informações atualizadas com sucesso.", extra_tags='alert-success alert-dismissible')
			
			return redirect('transac:tag_list')
		else:
			messages.error(request, "Foram preenchidos dados incorretamente.", extra_tags='alert-error alert-dismissible')               
	else:
		form = TagFormView(instance=tag)        

	args = {'form': form}    

	return render(request, 'transac/transac_edit.html', args)

def Tag_Del(request):
    if request.POST and request.is_ajax():        
        if request.POST.getlist('tag_lista[]'):
            tag_list = request.POST.getlist('tag_lista[]')            
            for i in tag_list:
                tag = Tag.objects.get(pk=i)
                tag.delete()            
            messages.success(request, "Mensagens excluidas com sucesso.", extra_tags='alert-success alert-dismissible')            
        else:
            messages.error(request, "Nenhuma mensagem selecionada.", extra_tags='alert-error alert-dismissible')               

    return HttpResponse('')
