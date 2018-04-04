from django.conf.urls import url, include
from django.urls import resolve
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView,
    PasswordChangeDoneView,
)
from Repmuni import views
from Repmuni.views import UploadPhotosView, DetailPhotoView, UploadPhotoView
from Repmuni.forms import AuthenticationForm_CDGRD

#app_name = 'repmuni'

urlpatterns = [

    url(r'^reporte/$', views.Reporte, name='reporte'),
    url(r'^reporteReal/$', views.ReporteReal.as_view(), name='reporte_real'),
    url(r'^reporteRealfoto/$', UploadPhotoView.as_view(), name='reporte_real_foto'),
    url(r'^mapa/$', views.Mapa, name='mapa'),
    url(r'^photo/(?P<pk>\d+)/$', DetailPhotoView.as_view(), name='detail'),
    url(r'^register/$', views.register, name='register'),
    url(r'^profile/$', views.view_profile, name='profile'),
    url(r'^profile/edit$', views.edit_profile, name='profile_edit'),
    
    url('^', include('django.contrib.auth.urls')),

    url(r'^login/$', LoginView.as_view(authentication_form=AuthenticationForm_CDGRD), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    
    url(r'^password-change/$', PasswordChangeView.as_view(success_url='done/'), name='password_change'),
    url(r'^password-change/done/$', PasswordChangeDoneView.as_view(), name='password_change_done'),
    
    url(r'^reset-password/$', PasswordResetView.as_view(success_url='done/'), name='reset_password'),
    url(r'^reset-password/done/$', PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)/(?P<token>[0-9A-Za-z]{1,3}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmView.as_view(success_url='/repmuni/reset-password/complete/'), name='password_reset_confirm'),
    url(r'^reset-password/complete/$', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    ]
