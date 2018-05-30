from django.conf.urls import url
from . import views

app_name = 'ponto'
urlpatterns = [    
	url(r'^$', views.Ponto_List, name="ponto_list"),
	url(r'^add/$', views.Ponto_Add, name="ponto_add"),
	url(r'^view/(?P<pk>\d+)/$', views.Ponto_View, name='ponto_view'),
    url(r'^edit/(?P<pk>\d+)/$', views.Ponto_Edit, name='ponto_edit'),
    url(r'^del/$', views.Ponto_Del, name='ponto_del'),
    url(r'^paramponto/$', views.ParamPonto_Edit, name='paramponto_edit'),
    
]