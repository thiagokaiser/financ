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
import datetime
import calendar

# Create your views here.
def Ponto_List(request):
	ponto = Ponto.objects.filter(usuario=request.user)
	args = {'ponto': ponto}

	return render(request, 'ponto/ponto.html', args)

def Ponto_Add(request):
	if request.method == 'POST':
		form = PontoForm(request.POST)
		if form.is_valid():  
			ponto = form.save(commit=False)           				
			ponto.usuario = request.user
			ponto.save()
			messages.success(request, "Informações atualizadas com sucesso.", extra_tags='alert-success alert-dismissible')			
			return redirect('ponto:ponto_list')
		else:
			messages.error(request, "Foram preenchidos dados incorretamente.", extra_tags='alert-error alert-dismissible')               
	else:
		form = PontoForm()

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
		form = PontoForm(request.POST, instance=ponto)        
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