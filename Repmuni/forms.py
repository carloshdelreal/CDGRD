from django import forms
from django.forms import ModelForm
from django.utils import html
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordResetForm
from .models import Report, ReportAlbums, Photos, UserProfile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Div
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

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user

class EditProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
        ]
class EditUserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "description",
            "city",
            "website",
            "phone",
            "image",
        ]
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            HTML("""{% if UserProfile.image.url != null %}<img class="img-responsive" src="{{ UserProfile.image.url }}">{% endif %}"""),
        )
        super(EditUserProfileForm, self).__init__(*args, **kwargs)

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