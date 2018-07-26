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
                                      usuario=request.user).exclude(fixa=True)

	despesas_fixa = Despesa.objects.filter(fixa=True, 
										   usuario=request.user,
										   dt_vencimento__lte=datetime.datetime(ano,mes, 1) + datetime.timedelta(35))
	for despesa in despesas_fixa:				
		despesa.dt_vencimento = datetime.datetime(ano, mes, despesa.dt_vencimento.day)		
	for despesa in despesas:				
		despesas_fixa = despesas_fixa.exclude(pk=despesa.pk_fixa)
		
	despesas = despesas.exclude(eliminada=True)

	return despesas, despesas_fixa


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

