from django.conf.urls import url
from django.contrib.auth.views import (
	login,
	logout,
	password_reset,
	password_reset_done,
	password_reset_confirm,
	password_reset_complete,
	)

from . import views

app_name = 'app'
urlpatterns = [
    url(r'^$', views.Home, name='home'),
    url(r'^login/$', login, {'template_name': 'accounts/login.html'}, name='login'),        
    url(r'^logout/$', logout, {'template_name': 'accounts/logout.html'}, name='logout'), 
    url(r'^profile/$', views.Profile , name='profile'),
    url(r'^profile/edit/$', views.Edit_profile , name='edit_profile'),
    url(r'^register/$', views.Register , name='register'),
    url(r'^change-password/$', views.Change_Password , name='change_password'),    
    url(r'^reset-password/$', password_reset, {'template_name': 'accounts/reset_password.html',
    										   'post_reset_redirect': 'app:password_reset_done', 
    										   'email_template_name': 'accounts/reset_password_email.html'},
    										    name='reset_password'),
    url(r'^reset-password/done/$', password_reset_done, {'template_name': 'accounts/reset_password_done.html'},
    													  name='password_reset_done'),
    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 
												password_reset_confirm,
												{'template_name': 'accounts/reset_password_confirm.html',
												 'post_reset_redirect': 'app:password_reset_complete'},
												  name='password_reset_confirm'),
    url(r'^reset-password/complete/$', password_reset_complete,{'template_name': 'accounts/reset_password_complete.html'}, 
												                 name='password_reset_complete'),
    url(r'^inbox/$', views.Inbox , name='inbox'),
    url(r'^msg/(?P<pk>\d+)/$', views.Msg_View , name='msg'),
    url(r'^new_msg/$', views.New_Msg , name='new_msg'),
    url(r'^del_msg/$', views.Del_Msg , name='del_msg'),    
    url(r'^read_msg/$', views.Read_Msg , name='read_msg'),    
    url(r'^unread_msg/$', views.Unread_Msg , name='unread_msg'),    
    url(r'^side_menu/$', views.Side_Menu , name='side_menu'),    
]
