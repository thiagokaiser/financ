from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .forms import(
	PontoForm,
	PontoFormView,
	)
from .models import(
	Ponto,
	)
from django.utils import timezone
from django.contrib import messages
from django.core import serializers
from datetime import datetime, timedelta
import calendar
#import pdb; pdb.set_trace()
# Create your views here.
def Ponto_List(request):
	dia = datetime.today() - timedelta(days=10)
	p_dt_ini    = request.GET.get('dt_ini', dia.strftime('%Y-%m-%d'))
	p_dt_fim    = request.GET.get('dt_fim', datetime.today().strftime('%Y-%m-%d'))

	periodo = {'dt_ini': p_dt_ini,
               'dt_fim': p_dt_fim}

	#import pdb; pdb.set_trace()

	ponto = Ponto.objects.filter(usuario=request.user,
								 dia__range=(p_dt_ini, p_dt_fim))	
	ponto = ponto.order_by('dia','hora')
	args = {'ponto': ponto,
			'periodo':periodo}

	return render(request, 'ponto/ponto.html', args)

def Ponto_Add(request):
	if request.method == 'POST':
		form = PontoForm(request.POST, request.FILES)
		if form.is_valid():
			ponto = form.save(commit=False)
			ponto.usuario = request.user
			ponto.save()
			messages.success(request, "Informações atualizadas com sucesso.", extra_tags='alert-success alert-dismissible')			
			return redirect('ponto:ponto_list')
		else:
			messages.error(request, "Foram preenchidos dados incorretamente.", extra_tags='alert-error alert-dismissible')               
	else:
		data = {'dia': datetime.today().strftime('%Y-%m-%d'),
				'hora': datetime.today().strftime('%H:%M')}
		form = PontoForm(initial=data)

	args = {'form': form}

	return render(request, 'ponto/ponto_add.html', args)

def Ponto_View(request,pk):	
	ponto = get_object_or_404(Ponto, pk=pk)  	
	if ponto.usuario != request.user:
		messages.error(request, "Acesso negado!", extra_tags='alert-error alert-dismissible')			
		return redirect('ponto:ponto_list')

	form = PontoFormView(instance=ponto)    

	args = {'ponto': ponto, 'form': form}

	return render(request, 'ponto/ponto_view.html', args)

def Ponto_Edit(request,pk):
	ponto = get_object_or_404(Ponto, pk=pk)
	if ponto.usuario != request.user:
		messages.error(request, "Acesso negado!", extra_tags='alert-error alert-dismissible')			
		return redirect('ponto:ponto_list')
	if request.method == 'POST':
		form = PontoForm(request.POST, request.FILES, instance=ponto)        
		if form.is_valid():
			form.save()
			messages.success(request, "Informações atualizadas com sucesso.", extra_tags='alert-success alert-dismissible')
			return redirect('ponto:ponto_list')
		else:
			messages.error(request, "Foram preenchidos dados incorretamente.", extra_tags='alert-error alert-dismissible')
	else:						
		form = PontoForm(instance=ponto)
	args = {'form': form, 'ponto': ponto}

	return render(request, 'ponto/ponto_edit.html', args)

def Ponto_Del(request):
    if request.POST and request.is_ajax():        
        if request.POST.getlist('ponto_lista[]'):
            ponto_list = request.POST.getlist('ponto_lista[]')            
            for i in ponto_list:
                ponto = Ponto.objects.get(pk=i)
                if ponto.usuario != request.user:
                    messages.error(request, "Acesso negado!", extra_tags='alert-error alert-dismissible')			
                    return redirect('ponto:ponto_list')
                ponto.delete()            
            messages.success(request, "Ponto excluido com sucesso.", extra_tags='alert-success alert-dismissible')            
        else:
            messages.error(request, "Nenhum ponto selecionado.", extra_tags='alert-error alert-dismissible')               

    return HttpResponse('')
