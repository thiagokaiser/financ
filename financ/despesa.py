from .models import Despesa
from django.contrib import messages
import datetime

def AlteraDespesasPend(chave):	
	despesa_pai = Despesa.objects.get(pk = chave)
	if despesa_pai.pk_fixa != 0:		
		despesas = Despesa.objects.filter(pk = despesa_pai.pk_fixa).exclude(pago=True)
	else:
		despesas = Despesa.objects.filter(pk_fixa = chave).exclude(pago=True)	
	
	despesas.update(valor		   = despesa_pai.valor,
					descricao	   = despesa_pai.descricao,
					dt_vencimento  = despesa_pai.dt_vencimento,
					categoria	   = despesa_pai.categoria,
					pago		   = despesa_pai.pago,
					)

def BuscaDespesasMes(request,ano,mes):
	despesas = Despesa.objects.filter(dt_vencimento__year=ano,
                                      dt_vencimento__month=mes,
                                      usuario=request.user)

	return despesas

def EliminaDespesa(request, url):
	if request.POST and request.is_ajax():        
		if request.POST.getlist('despesa_lista[]'):
			despesa_list = request.POST.getlist('despesa_lista[]')            
			for i in despesa_list:
				despesa = Despesa.objects.get(pk=i)
				if despesa.usuario != request.user:
					messages.error(request, "Acesso negado!", extra_tags='alert-error alert-dismissible')			
					return redirect('financ:despesas' + url)
				despesa.delete()            
			messages.success(request, "Despesas excluidas com sucesso.", extra_tags='alert-success alert-dismissible')            
		else:
			messages.error(request, "Nenhuma despesa selecionada.", extra_tags='alert-error alert-dismissible')   


def AdicionaDespesa(despesa,qtd_meses):
	i = 1
	dt_vencimento = despesa.dt_vencimento
	while i < qtd_meses:

		dt_vencimento = datetime.datetime(dt_vencimento.year, dt_vencimento.month + 1, dt_vencimento.day) 

		Despesa.objects.create(valor		  = despesa.valor,
							   descricao	  = despesa.descricao + str(qtd_meses),
							   dt_vencimento  = dt_vencimento,
							   categoria	  = despesa.categoria,
							   pago		      = False,
							   fixa           = False,
							   pk_fixa        = despesa.pk,
							   usuario        = despesa.usuario
							   )
		i = i + 1

def EditaDespesa(request,despesa,tipo):
	pass