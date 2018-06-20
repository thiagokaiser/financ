from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .forms import(
	PontoForm,
	PontoFormView,
	ParamPontoForm,
	)
from .models import(
	Ponto,
	ParamPonto,
	)
from django.utils import timezone
from django.contrib import messages
from django.core import serializers
from datetime import datetime, timedelta, date
import calendar
#import pdb; pdb.set_trace()
# Create your views here.
def Ponto_List(request):
	dia = datetime.today() - timedelta(days=10)
	p_dt_ini    = request.GET.get('dt_ini', dia.strftime('%Y-%m-%d'))
	p_dt_fim    = request.GET.get('dt_fim', datetime.today().strftime('%Y-%m-%d'))
	p_rs_ponto  = request.GET.get('rs_ponto', 'all')

	periodo = {'dt_ini': p_dt_ini,
               'dt_fim': p_dt_fim}

	#import pdb; pdb.set_trace()

	ponto = Ponto.objects.filter(usuario=request.user,
								 dia__range=(p_dt_ini, p_dt_fim))	
	ponto = ponto.order_by('dia','hora')
	
	try:
	    paramponto = ParamPonto.objects.get(usuario=request.user)
	except ParamPonto.DoesNotExist:
	    paramponto = None
	if not paramponto:
		paramponto = ParamPonto.objects.create(usuario=request.user,
								  entrada="07:30",
								  saida="17:18",
								  tolerancia="00:00")

	parampontoform = ParamPontoForm(instance=paramponto)	

	for i in ponto:	
		i.exc = False	
		if i.tipo == 'entrada':			
			v_entrad   = timedelta(hours=paramponto.entrada.hour,minutes=paramponto.entrada.minute) + timedelta(hours=paramponto.tolerancia.hour,minutes=paramponto.tolerancia.minute)
			v_entrad_l = timedelta(hours=paramponto.entrada.hour,minutes=paramponto.entrada.minute) - timedelta(hours=paramponto.tolerancia.hour,minutes=paramponto.tolerancia.minute)
			if v_entrad < timedelta(hours=i.hora.hour,minutes=i.hora.minute):
				i.banco = timedelta(hours=i.hora.hour,minutes=i.hora.minute) - timedelta(hours=paramponto.entrada.hour,minutes=paramponto.entrada.minute)
				i.cor = "red"
				i.exc = True		
			elif v_entrad_l > timedelta(hours=i.hora.hour,minutes=i.hora.minute):
				i.banco = timedelta(hours=paramponto.entrada.hour,minutes=paramponto.entrada.minute) - timedelta(hours=i.hora.hour,minutes=i.hora.minute)
				i.cor = "green"		
				i.exc = True		
		else:
			v_saida   = timedelta(hours=paramponto.saida.hour,minutes=paramponto.saida.minute) + timedelta(hours=paramponto.tolerancia.hour,minutes=paramponto.tolerancia.minute)
			v_saida_l = timedelta(hours=paramponto.saida.hour,minutes=paramponto.saida.minute) - timedelta(hours=paramponto.tolerancia.hour,minutes=paramponto.tolerancia.minute)
			if v_saida < timedelta(hours=i.hora.hour,minutes=i.hora.minute):
				i.banco = timedelta(hours=i.hora.hour,minutes=i.hora.minute) - timedelta(hours=paramponto.saida.hour,minutes=paramponto.saida.minute)
				i.cor = "green"		
				i.exc = True		
			elif v_saida_l > timedelta(hours=i.hora.hour,minutes=i.hora.minute):
				i.banco = timedelta(hours=paramponto.saida.hour,minutes=paramponto.saida.minute) - timedelta(hours=i.hora.hour,minutes=i.hora.minute) 
				i.cor = "red"		
				i.exc = True		

	#import pdb; pdb.set_trace()

	args = {'ponto': ponto,
			'periodo':periodo,
			'paramponto': parampontoform,
			'parampontoform': paramponto,
			'p_rs_ponto': p_rs_ponto}

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

def ParamPonto_Edit(request):
	if request.is_ajax():
		if request.method == 'POST':
			paramponto = ParamPonto.objects.get(usuario=request.user)
			form = ParamPontoForm(request.POST, instance=paramponto)
			if form.is_valid():				
				form.save()				
			
			return HttpResponse('')   