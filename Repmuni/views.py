from django.shortcuts import render, redirect
from Repmuni.forms import FormLogin, RegistrationForm, EditProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
#from django.contrib.auth.decorators import login_required
from django.contrib.auth import user_logged_in
from django.contrib.auth.models import User
# Create your views here.
from django.views.generic.edit import FormView
from django.views.generic import DetailView
from django.views import View
from .forms import ReportForm, PhotosForm
from .models import Photos

def Reporte(request):
    return render(request, 'Repmuni/reporte_anonimo.html')

class ReporteReal(FormView):
    template_name = 'Repmuni/mapa_reporte.html'
    form_class = ReportForm
    success_url = '/mapa/'
    def form_valid(self, form):
        return super().form_valid(form)

class UploadPhotoView(View):
    template_name = 'Repmuni/mapa_reporte.html'
    form_class = PhotosForm
    success_url = 'Repmuni'
    def get(self, request):
        context = {
            "form": self.form_class()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = PhotosForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(Photos.objects.order_by('-pk')[0])

class DetailPhotoView(DetailView):
    model = Photos
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def Mapa(request):
    return render(request, 'Repmuni/mapa.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            form_register = RegistrationForm()
            return render(request, 'Repmuni/registro_exitoso.html')
        else:
            # Return an 'Invalid Login' error message
            form_register = RegistrationForm()
            context = {'welcome': 'Mal Password',
                       'form_register': form_register
                       }
            return render(request, 'Repmuni/register.html', context)
    else:
        form_register = RegistrationForm()
        context = {'form_register': form_register}
        return render(request, 'Repmuni/register.html', context)

def view_profile(request):
    return render(request, 'Repmuni/profile.html')

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/profile')
    else:
        form = EditProfileForm(instance=request.user)
        context = {'form': form}
        return render(request, 'Repmuni/profile_edit.html',context)

def Password_Change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/profile')
        else:
            redirect('/password_change')
    else:
        form = PasswordChangeForm(user=request.user)
        context = {'form': form}
        return render(request, 'Repmuni/password_change.html',context)