from django.db import models

# Create your models here.
class Despesa(models.Model):
	valor			= models.DecimalField(max_digits=12, decimal_places=2)	
	descricao		= models.CharField(max_length=40, blank=True)		
	dt_vencimento	= models.DateField()			
	categoria		= models.ForeignKey('Categoria', on_delete=models.PROTECT)
	pago			= models.BooleanField(default=False)
	fixa            = models.BooleanField(default=False)
	pk_fixa         = models.IntegerField(blank=True, default=0)
	def __str__(self):
		return self.descricao

class Categoria(models.Model):
	descricao		= models.CharField(max_length=40, unique=True)
	cor     		= models.CharField(max_length=40, blank=True)
	def __str__(self):
		return self.descricao