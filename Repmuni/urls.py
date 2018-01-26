from django.conf.urls import url
from Repmuni import views
from django.contrib.auth.views import (
    login, logout, password_reset, password_reset_done, password_reset_confirm,
    password_reset_complete
)


#app_name = 'repmuni'

urlpatterns = [

    url(r'^reporte/$', views.Reporte, name='reporte'),
    url(r'^mapa/$', views.Mapa, name='mapa'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', login, {'template_name': 'Repmuni/login.html'}, name='login'),
    url(r'^logout/$', logout, {'template_name': 'Repmuni/logout.html'}, name='logout'),
    url(r'^profile/$', views.view_profile, name='profile'),
    url(r'^profile/edit$', views.edit_profile, name='profile_edit'),
    url(r'^change-password/$', views.Password_Change, name='password_change'),

    url(r'^reset-password/$', password_reset,{'template_name':'Repmuni/reset_password.html',
                                              'post_reset_redirect':'repmuni:password_reset_done',
                                              'email_template_name':'repmuni/reset_password_email.html'
                                              }, name='reset_password'),

    url(r'^reset-password/done/$', password_reset_done, {'template_name':'repmuni/reset_password_done.html'
                                                         } , name='password_reset_done'),

    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        password_reset_confirm, {'template_name': 'Repmuni/reset_password_confirm.html',
                                 'post_reset_redirect':'repmuni:password_reset_complete'
                                 }, name='password_reset_confirm'),
    #python -m smtpd -n -c DebuggingServer localhost:1025
    #EMAIL_HOST = 'localhost'
    #EMAIL_PORT = 1025
    url(r'^reset-password/complete/$', password_reset_complete,
        {'template_name':'Repmuni/reset_password_complete.html'
         }, name='password_reset_complete')
    ]
