from .models import Despesa, Categoria
from django.contrib import messages
from django.db.models import Sum
from io import StringIO, BytesIO
import datetime
import xlsxwriter
from decimal import *
import itertools
#import pdb; pdb.set_trace()

def funcao_data(i):
    array = []
    dt = datetime.datetime.today()
    array.append(dt)
    while i > 0:
        prev = dt.replace(day=1) - datetime.timedelta(days=1)
        dt = prev        
        array.append(prev)
        i = i - 1
    return array

def HomeDespesa(request,data):
    #despesas = Despesa.objects.all()
        
    home = dict()
    home['data'] = data
        
    #----- GERAR GRAFICO BARRA ----------    
    pagtomes = Despesa.objects.filter(usuario=request.user,pago=True).values('dt_vencimento','valor').order_by('dt_vencimento')
    pagtomesgrp = itertools.groupby(pagtomes, lambda d: d.get('dt_vencimento').strftime('%Y-%m'))    
    pagtomesresult = [{'mes': month, 'valor': sum([x['valor'] for x in this_day])} 
        for month, this_day in pagtomesgrp]

    teste = funcao_data(11)
    newdict = dict()
    arraydict = []

    for arraydata in teste:
        mes = arraydata.strftime('%Y-%m')
        valor = 0
        for i in pagtomesresult:        
            if mes == i['mes']:
                valor = i['valor']        
        newdict = {'mes': mes , 'valor': valor}
        arraydict.append(newdict)    

    home['pagtomes'] = arraydict
    #------------------------------------

    #----- GERAR GRAFICO PIZZA ----------
    despesas_pie = Despesa.objects.filter(usuario=request.user,
                                      pago=True,
                                      dt_vencimento__month=data.month,
                                      dt_vencimento__year=data.year).values('categoria__descricao','valor').order_by('categoria')

    despesasgrp = itertools.groupby(despesas_pie, lambda d: d.get('categoria__descricao'))

    despesasresult = [{'categoria': categoria, 'valor': sum([x['valor'] for x in this_day])} 
        for categoria, this_day in despesasgrp]       
    
    for i in despesasresult:
        categ = Categoria.objects.get(descricao=i.get('categoria'))        
        i['cor'] = categ.cor

    home['despesas'] = despesasresult
    #------------------------------------     
    
    despesas = Despesa.objects.filter(usuario=request.user,
                                      dt_vencimento__month=data.month,
                                      dt_vencimento__year=data.year)
    
    for despesa in despesas:        
        if despesa.pago == True:
            home['pagto'] = home.get('pagto', 0) + despesa.valor                
        home['total'] = home.get('total', 0) + despesa.valor                
    if home.get('total', 0) != 0:
        home['percent'] =  round((home.get('pagto', 0) * 100) / home.get('total', 0), 0)
    else:
        home['percent'] =  0

    home['desp_pend'] = despesas.filter(pago=False)
    home['desp_paga'] = despesas.filter(pago=True)
    
    args = {'home': home} 
    return args

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

	pago = Despesa.objects.filter(dt_vencimento__year=ano,
                                   dt_vencimento__month=mes,
                                   usuario=request.user,
                                   pago=True).aggregate(Sum("valor"))

	pendente = Despesa.objects.filter(dt_vencimento__year=ano,
                                   dt_vencimento__month=mes,
                                   usuario=request.user,
                                   pago=False).aggregate(Sum("valor"))


	total = float(pago['valor__sum'] or 0) + float(pendente['valor__sum'] or 0)

	totais = {'pago': float(pago['valor__sum'] or 0),
			  'pendente': float(pendente['valor__sum'] or 0),
			  'total': total}


	return despesas, totais

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


def GeraExcel(despesas):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)   

    # excel styles
    title = workbook.add_format({
        'bold': True,
        'font_size': 14,
        'align': 'center',
        'valign': 'vcenter'
    })
    header = workbook.add_format({
        'bold': True,
        'bg_color': '#337ca5',
        'color': 'white',
        'align': 'center',
        'valign': 'top',
        'border': 1
    })
    cell = workbook.add_format({
        'align': 'left',
        'valign': 'top',
        'text_wrap': True,
        'border': 1
    })
    cell_center = workbook.add_format({
        'align': 'center',
        'valign': 'top',
        'border': 1
    })
    cell_valor = workbook.add_format({
        'num_format': 'R$ #,##0.00;[Red]R$ #,##0.00',
        'valign': 'top',
        'border': 1
    })

    worksheet_s = workbook.add_worksheet('Despesas')
    title_text = 'Despesas'

	# merge cells
    worksheet_s.merge_range('A2:F2', title_text, title)

    # write header
    worksheet_s.write(3, 0, "Pago?", header)
    worksheet_s.write(3, 1, "Descrição", header)
    worksheet_s.write(3, 2, "Categoria", header)
    worksheet_s.write(3, 3, "Parcela", header)   
    worksheet_s.write(3, 4, "Dt Vencimento", header)
    worksheet_s.write(3, 5, "Valor(R$)", header)        

    row = 4

    for despesa in despesas: 

        worksheet_s.write(row, 0, str('Sim' if despesa.pago is True else 'Não'), cell)
        worksheet_s.write_string(row, 1, despesa.descricao, cell)
        worksheet_s.write_string(row, 2, despesa.categoria.descricao, cell)
        worksheet_s.write_string(row, 3, despesa.parcela, cell)
        worksheet_s.write_string(row, 4, despesa.dt_vencimento.strftime('%d/%m/%Y'), cell_center)
        worksheet_s.write_number(row, 5, Decimal(despesa.valor or 0), cell_valor)
                
        # change column widths
        worksheet_s.set_column('A:A', 15)  
        worksheet_s.set_column('B:B', 15)  
        worksheet_s.set_column('C:C', 15)          
        worksheet_s.set_column('D:D', 15)  
        worksheet_s.set_column('E:E', 15)  
        worksheet_s.set_column('F:F', 15)      

        row = row + 1

    # close workbook
    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data