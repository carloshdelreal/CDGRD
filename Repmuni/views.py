from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, user_logged_in
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.views import PasswordResetCompleteView
#from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.views.generic.edit import FormView, CreateView
from django.views.generic import DetailView, ListView
from django.views import View
from .models import Photos, UserProfile, Report
from .forms import (
    RegistrationForm, EditProfileForm, EditUserProfileForm,
    ReportForm, PhotosForm, UploadPhotosFormset, PhotosFormSet
)

def Reporte(request):
    return render(request, 'Repmuni/reporte_anonimo.html')

class ReportList(ListView):
    template_name = 'report_list.html'
    def get_queryset(self):
        return Report.objects.filter(user=self.request.user)

class NuevoReporteReal(FormView):
    template_name = 'Repmuni/mapa_reporte_nuevo.html'
    form_class = ReportForm
    success_url = "/repmuni/reporteLista/"
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(NuevoReporteReal, self).form_valid(form)

class ReporteReal(View):
    template_name = 'Repmuni/mapa_reporte.html'
    form = ReportForm
    formset = PhotosFormSet
    def get(self, request):
        context = {
            "form": self.form,
            "formset": self.formset,
        }
        return render(request, self.template_name, context)
    def post(self, request):
        form = self.form(request.POST)
        formset = self.formset(request.POST, request.FILES)
        if form.is_valid():
            r = form.save(commit=False)
            r.user = request.user
            r.save()
            for form in formset:
                if form.is_valid():
                    p = form.save(commit=False)
                    p.report = r
                    p.save()
            return redirect("/repmuni/reportelista/")
        return render(request, self.template_name, {"form": self.form,'formset': formset})

class ReportDetail(DetailView):
    model = Report
    template_name = "Repmuni/report_detail.html"
    def get_context_data(self, **kwargs):
        context = super(ReportDetail, self).get_context_data(**kwargs)
        context['photos'] = get_list_or_404(Photos, report=self.kwargs['pk'])
        return context

class PhotoDetail(DetailView):
    model = Photos
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photo'] = get_object_or_404(Photos, pk=self.kwargs['pk'])
        return context

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
    formset_obj = UploadPhotosFormset

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
