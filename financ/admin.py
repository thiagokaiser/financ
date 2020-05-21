from django.contrib import admin
from .models import Despesa, Categoria, Importacao, Conta

admin.site.register(Despesa)
admin.site.register(Categoria)
admin.site.register(Importacao)
admin.site.register(Conta)