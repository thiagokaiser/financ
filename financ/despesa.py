from .models import Despesa
from django.contrib import messages
import datetime

def AlteraDespesasPend(despesa):		

	despesas = Despesa.objects.filter(pk_fixa = despesa.pk_fixa).exclude(pago=True)			

	despesas.update(valor		   = despesa.valor,
					descricao	   = despesa.descricao,					
					categoria	   = despesa.categoria,					
					)

def BuscaDespesasMes(request,ano,mes):
	despesas = Despesa.objects.filter(dt_vencimento__year=ano,
                                      dt_vencimento__month=mes,
                                      usuario=request.user)

	return despesas

def EliminaDespesa(request, param):
	if request.POST and request.is_ajax():        
		if request.POST.getlist('despesa_lista[]'):
			despesa_list = request.POST.getlist('despesa_lista[]')            
			for i in despesa_list:

				if param == 1:
					despesa = Despesa.objects.filter(pk=i)
				else:					
					despesa = Despesa.objects.filter(pk_fixa = i).exclude(pago=True)				

				if despesa[0].usuario != request.user:
					messages.error(request, "Acesso negado!", extra_tags='alert-error alert-dismissible')													
				else:
					despesa.delete()            

			messages.success(request, "Despesas excluidas com sucesso.", extra_tags='alert-success alert-dismissible')            
		else:
			messages.error(request, "Nenhuma despesa selecionada.", extra_tags='alert-error alert-dismissible')   


def AdicionaDespesa(despesa,qtd_meses):

	despesa_pai = Despesa.objects.filter(pk=despesa.pk)
	despesa_pai.update(pk_fixa = despesa.pk)

	i = 1
	dt_vencimento = despesa.dt_vencimento
	while i < qtd_meses:
		i = i + 1

		if dt_vencimento.month + 1 == 13:
			dt_vencimento = datetime.datetime(dt_vencimento.year + 1, 1, dt_vencimento.day) 
		else:
			dt_vencimento = datetime.datetime(dt_vencimento.year, dt_vencimento.month + 1, dt_vencimento.day) 

		Despesa.objects.create(valor		  = despesa.valor,
							   descricao	  = despesa.descricao,
							   dt_vencimento  = dt_vencimento,
							   categoria	  = despesa.categoria,
							   pago		      = False,
							   fixa           = True,
							   pk_fixa        = despesa.pk,
							   usuario        = despesa.usuario,
							   parcela        = str(i) + '/' + str(qtd_meses)
							   )
		

def EditaDespesa(request,despesa,tipo):
	pass