from django.contrib import admin

# Register your models here.
from .models import Despesa, Categoria

admin.site.register(Despesa)
admin.site.register(Categoria)