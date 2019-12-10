from django.conf.urls import url
from . import views

app_name = 'financ'
urlpatterns = [    
	url(r'^$', views.Despesas, name="despesas"),
    url(r'^add/$', views.Despesa_Add, name='despesa_add'),    
    url(r'^view/(?P<pk>\d+)/$', views.Despesa_View, name='despesa_view'),
    url(r'^edit/(?P<pk>\d+)/$', views.Despesa_Edit, name='despesa_edit'),
    url(r'^edit_all/(?P<pk>\d+)/$', views.Despesa_Edit_All, name='despesa_edit_all'),
    url(r'^del/$', views.Despesa_Del, name='despesa_del'),
    url(r'^del_all/$', views.Despesa_Del_All, name='despesa_del_all'),
    url(r'^gera_xls_mes/$', views.Gera_XLS_Mes, name='gera_xls_mes'),
    url(r'^categoria_add/$', views.Categoria_Add, name='categoria_add'),        
    url(r'^categoria_list/$', views.Categoria_List, name='categoria_list'),        
    url(r'^categoria_view/(?P<pk>\d+)/$', views.Categoria_View, name='categoria_view'),        
    url(r'^categoria_edit/(?P<pk>\d+)/$', views.Categoria_Edit, name='categoria_edit'),        
    url(r'^categoria_del/$', views.Categoria_Del, name='categoria_del'),
    url(r'^conta_add/$', views.Conta_Add, name='conta_add'),        
    url(r'^conta_list/$', views.Conta_List, name='conta_list'),        
    url(r'^conta_view/(?P<pk>\d+)/$', views.Conta_View, name='conta_view'),        
    url(r'^conta_edit/(?P<pk>\d+)/$', views.Conta_Edit, name='conta_edit'),        
    url(r'^conta_del/$', views.Conta_Del, name='conta_del'),
]