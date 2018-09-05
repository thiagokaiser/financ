from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Despesa(models.Model):
	valor			= models.DecimalField(max_digits=12, decimal_places=2)	
	descricao		= models.CharField(max_length=40, blank=True)		
	dt_vencimento	= models.DateField()			
	categoria		= models.ForeignKey('Categoria', on_delete=models.PROTECT)
	pago			= models.BooleanField(default=False)
	fixa            = models.BooleanField(default=False)
	pk_fixa         = models.IntegerField(blank=True, default=0)
	usuario         = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	eliminada       = models.BooleanField(default=False)
	parcela         = models.CharField(max_length=10, blank=True)		
	importacao      = models.ForeignKey('Importacao', on_delete=models.CASCADE, null=True)
	def __str__(self):
		return self.descricao

class Categoria(models.Model):
	descricao		= models.CharField(max_length=40)
	cor     		= models.CharField(max_length=40, blank=True)
	usuario         = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	def __str__(self):
		return self.descricao

class Importacao(models.Model):
	descricao = models.CharField(max_length=40)
	dt_import = models.DateField()			
	usuario   = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	def __str__(self):
		return self.descricao