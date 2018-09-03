import csv
from django.contrib.auth.models import User
from financ.models import Despesa, Categoria

#teste = Despesa.objects.all()

#for i in teste:
#	print(i.categoria)

with open('financ./scripts./despesas.csv') as csvfile:
	reader = csv.DictReader(csvfile, delimiter=';')

	for row in reader:
		#print(row['Data'], row['descricao'], row['Categoria'], row['Valor'].replace('R$',''))		
		categ = Categoria.objects.get(descricao=row['Categoria'])
		user  = User.objects.get(username='kaiser')

		valor = row['Valor'].replace('R$','')
		valor = valor.replace('.','')
		valor = valor.replace(',','.')

		print(categ.pk, user.pk)
		
		Despesa.objects.create(valor		  = valor,
							   descricao	  = row['descricao'],
							   dt_vencimento  = row['Data'],
							   categoria	  = categ,
							   pago		      = True,
							   fixa           = False,							   
							   usuario        = user,							   
							   )
		