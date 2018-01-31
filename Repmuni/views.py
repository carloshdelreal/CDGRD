from django.shortcuts import render, redirect
from Repmuni.forms import FormLogin, RegistrationForm, EditProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
#from django.contrib.auth.decorators import login_required
from django.contrib.auth import user_logged_in
from django.contrib.auth.models import User
# Create your views here.

def Reporte(request):
    return render(request, 'Repmuni/reporte_anonimo.html')

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
    context = {'user': request.user}
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