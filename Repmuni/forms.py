from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordResetForm
from .models import Report, ReportAlbums, Photos
#from django.db import models

class AuthenticationForm_CDGRD(AuthenticationForm):
    AuthenticationForm.error_messages = {'invalid_login': 'Ingrese un password y contraseña correcta, verifique mayusculas y minúsculas',
        'inactive': 'Esta cuenta está inactiva'}
    AuthenticationForm.base_fields['username'].widget.attrs.update({'class': "form-control"})
    AuthenticationForm.base_fields['password'].widget.attrs.update({'class': "form-control"})
    class Meta:
        model = User
        fields = ['username', 'password']
        
class RegistrationForm(UserCreationForm):
    
    UserCreationForm.error_messages = {
        'password_mismatch': "Los Passwords no coinciden"
    }
    UserCreationForm.base_fields["password1"].help_text = (
        '<ul><li>Su password no puede ser similar a su información personal</li>'
            '<li>Debe contener al menos 8 caracteres</li>'
            '<li>No debe ser usado comunmente</li>'
            '<li>No debe ser enteramente numérico</li>'
        '</ul>'
    )
    UserCreationForm.base_fields["password1"].widget.attrs.update({'class': "form-control"})
    UserCreationForm.base_fields["password2"].widget.attrs.update({'class': "form-control"})
    #print(type(UserCreationForm.base_fields["password1"].widget_attrs))
    
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2"
        ]
        help_texts = {
            "username": "",
            "password1": "",
            "password2": "",
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': "form-control", "placeholder": "pepitoperez"}),
            'first_name': forms.TextInput(attrs={'class': "form-control", "placeholder": "Pepito"}),
            'last_name': forms.TextInput(attrs={'class': "form-control", "placeholder": "Pérez"}),
            'email': forms.EmailInput(attrs={'class': "form-control", "placeholder": "pepitoperez@gmail.com"}),
        }

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user

class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "password"
        ]

class PasswordResetFormCDGRD(PasswordResetForm):
    PasswordResetForm.base_fields["email"].widget.attrs.update({'class': "form-control"})

class PhotosForm(ModelForm):
    class Meta:
        model = Photos
        fields = [
            "image",
            "imagedescription",
        ]
        label = {
            "imagedescription": "Descripción de la Imágen",
        }
        required = {
            "image": True,
            "imagedescription": True,
        }
        # initial = {
        #     "imagedescription": "Escriba una descripción de la Imágen"
        # }
        widgets = {
            'imagedescription': forms.Textarea(attrs={'rows': 3, 'class': "form-control", "placeholder": "Describa la Imágen"}),
        }
        # help_texts = {
        #     'imagedescription': 'Describa que intenta mostrar en la fotografía',
        # }
        # error_messages = {
        #     'imagedescription': {
        #         'max_length': "Esta descripción está muy larga :D",
        #     },
        # }


class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = [
            "title",
            "fenomena",
            "descrip",
            "photos",
        ]