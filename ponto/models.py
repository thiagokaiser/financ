from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Ponto(models.Model):
	usuario      = models.ForeignKey(User, on_delete=models.CASCADE,default='')
	dia          = models.DateField()			
	hora         = models.TimeField()			
	observacao   = models.CharField(max_length=40, blank=True)		
	tipo         = models.CharField(max_length=9,
                  					choices=(('entrada','Entrada'),('saida','Saida')),
              						default="entrada")
	
	def __str__(self):
		retorno = self.dia + ' ' + self.hora
		return retorno