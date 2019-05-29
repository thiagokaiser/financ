from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
import os

# Create your models here.

class PontoUser(models.Manager):
	def get_queryset(self):
		qs = super(PontoUser, self).get_queryset()		
		return qs.filter(observacao='teste')

class Ponto(models.Model):
	usuario      = models.ForeignKey(User, on_delete=models.CASCADE,default='')
	dia          = models.DateField()
	hora         = models.TimeField()			
	observacao   = models.CharField(max_length=40, blank=True)		
	tipo         = models.CharField(max_length=9,
                  					choices=(('entrada','Entrada'),('saida','Saida')),
              						default="entrada")
	comprovante  = models.FileField(upload_to='ponto/comprovantes/', blank=True, null=True)

	def __str__(self):
		retorno = str(self.dia) + '  ' + str(self.hora)
		return retorno

	objects = models.Manager()
	objects_user = PontoUser()

	class Meta:
		permissions = (('acesso_app_ponto', 'Pode acessar Ponto'),
					   ('adicionar_anexo','Pode anexar foto'),)

class ParamPonto(models.Model):
    usuario      = models.ForeignKey(User, on_delete=models.CASCADE,default='')
    entrada      = models.TimeField()           
    saida        = models.TimeField()           
    tolerancia   = models.TimeField()           


@receiver(models.signals.post_delete, sender=Ponto)
def delete_file_on_del_pagto(sender, instance, **kwargs):    
    if instance.comprovante:
        if os.path.isfile(instance.comprovante.path):
            os.remove(instance.comprovante.path)

@receiver(models.signals.pre_save, sender=Ponto)
def delete_file_on_change_pagto(sender, instance, **kwargs):    
    if not instance.pk:
        return False

    try:
        old_file = Ponto.objects.get(pk=instance.pk).comprovante
    except Ponto.DoesNotExist:
        return False

    new_file = instance.comprovante
    if not old_file == new_file:
        if old_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)