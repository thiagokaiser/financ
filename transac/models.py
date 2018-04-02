from django.db import models

# Create your models here.
class Transacao(models.Model):
	valor			= models.DecimalField(max_digits=12, decimal_places=2)	
	descricao		= models.CharField(max_length=40, blank=True)		
	dt_vencimento	= models.DateField()			
	tag				= models.ForeignKey('Tag', on_delete=models.PROTECT)
	pago			= models.BooleanField(default=False)

class Tag(models.Model):
	descricao		= models.CharField(max_length=40)
	cor     		= models.CharField(max_length=40, blank=True)
	def __str__(self):
		return self.descricao