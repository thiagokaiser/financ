from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .forms import(
	PontoForm,
	)
from django.utils import timezone
from django.contrib import messages
from django.core import serializers
import datetime
import calendar

# Create your views here.
def Ponto(request):
	args = {}

	return render(request, 'ponto/ponto.html', args)

def Ponto_Add(request):
	if request.method == 'POST':
		form = PontoForm(request.POST)
		if form.is_valid():  
			ponto = form.save(commit=False)           				
			ponto.usuario = request.user
			ponto.save()
			messages.success(request, "Informações atualizadas com sucesso.", extra_tags='alert-success alert-dismissible')			
			return redirect('ponto:ponto')
		else:
			messages.error(request, "Foram preenchidos dados incorretamente.", extra_tags='alert-error alert-dismissible')               
	else:
		form = PontoForm()

	args = {'form': form}

	return render(request, 'ponto/ponto_add.html', args)