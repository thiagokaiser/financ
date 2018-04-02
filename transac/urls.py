from django.conf.urls import url
from . import views




app_name = 'transac'
urlpatterns = [    
	url(r'^$', views.Transacoes, name="transacoes"),
    url(r'^add/$', views.Transacao_Add, name='transacao_add'),    
    url(r'^view/(?P<pk>\d+)/$', views.Transacao_View, name='transacao_view'),
    url(r'^edit/(?P<pk>\d+)/$', views.Transacao_Edit, name='transacao_edit'),
    url(r'^tag_add/$', views.Tag_Add, name='tag_add'),        
    url(r'^tag_list/$', views.Tag_List, name='tag_list'),        
    url(r'^tag_view/(?P<pk>\d+)/$', views.Tag_View, name='tag_view'),        
    url(r'^tag_edit/(?P<pk>\d+)/$', views.Tag_Edit, name='tag_edit'),        
    url(r'^tag_del/$', views.Tag_Del, name='tag_del'),
]