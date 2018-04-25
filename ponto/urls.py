from django.conf.urls import url
from . import views

app_name = 'ponto'
urlpatterns = [    
	url(r'^$', views.Ponto, name="ponto"),
	url(r'^add/$', views.Ponto_Add, name="ponto_add"),
    
]