from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from .forms import RegistrationForm, EditProfileForm, EditUserProfileForm, ReportForm, PhotosForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, user_logged_in
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.views import PasswordResetCompleteView
#from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User
# Create your views here.
from django.views.generic.edit import FormView
from django.views.generic import DetailView
from django.views import View
from .models import Photos, UserProfile

def Reporte(request):
    return render(request, 'Repmuni/reporte_anonimo.html')

class ReporteReal(FormView):
    template_name = 'Repmuni/mapa_reporte.html'
    form_class = ReportForm
    success_url = '/mapa/'
    def form_valid(self, form):
        return super().form_valid(form)

class UploadPhotoView(View):
    template_name = 'Repmuni/mapa_reporte_foto.html'
    success_url = 'Repmuni'
    def get(self, request):
        form = PhotosForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PhotosForm(request.POST, request.FILES)
        if form.is_valid():
            #name = form.cleaned_data.get('name')
            form.save()
        return redirect(Photos.objects.order_by('-pk')[0])

class UploadPhotosView(View):
    template_name = 'Repmuni/mapa_reporte.html'
    formset_obj = modelformset_factory(Photos, PhotosForm)
    
    def get(self, request):
        formset = self.formset_obj(request.GET or None)
        return render(request, self.template_name, {'formset': formset})

    def post(self, request):
        formset = self.formset_obj(request.POST, request.FILES or None)
        #form = PhotosForm(request.POST, request.FILES)
        #print(request.FILES.keys())
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    #name = form.cleaned_data.get('name')
                    form.save()
            return redirect(Photos.objects.order_by('-pk')[0])
        return render(request, self.template_name, {'formset': formset})

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
            context = {
                'reg_user': request.POST['username'],
                'reg_email': request.POST['email'],
                'reg_name': request.POST['first_name'],
                'reg_lastName': request.POST['last_name'],
            }
            form.save()
            return render(request, 'registration/registro_exitoso.html', context)
        else:
            context = { 'form': form }
            return render(request, 'registration/register.html', context)
    else:
        form = RegistrationForm()
        context = {'form': form}
        return render(request, 'registration/register.html', context)

def view_profile(request):
    context = { 'UserProfile': UserProfile.objects.get(user=request.user) }
    return render(request, 'Repmuni/profile.html', context)

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        form_up = EditUserProfileForm(request.POST, request.FILES, instance=UserProfile.objects.get(user=request.user))
        if form.is_valid() and form_up.is_valid():
            form.save()
            form_up.save()
            return redirect('/repmuni/profile')
    else:
        UP = UserProfile.objects.get(user=request.user)
        form = EditProfileForm(instance=request.user)
        form_up = EditUserProfileForm(instance=UP)
        context = {'form': form, 'form_up': form_up, "UserProfile": UP}
        return render(request, 'Repmuni/profile_edit.html', context)

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

