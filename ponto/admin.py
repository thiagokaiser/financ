from django.contrib import admin

# Register your models here.
from .models import Ponto,ParamPonto

admin.site.register(Ponto)
admin.site.register(ParamPonto)