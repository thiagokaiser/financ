from .models import Despesa
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
		
	return despesas, despesas_fixa