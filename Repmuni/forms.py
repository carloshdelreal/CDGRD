from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
    UserCreationForm, UserChangeForm, AuthenticationForm, PasswordResetForm
)
from .models import Report, Photos, UserProfile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Field

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
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'

class EditUserProfileForm(forms.ModelForm):
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
        super(EditUserProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.layout.append( 
            HTML("""{% if UserProfile.image.url != null %}
                    <div class="col-md-7 col-md-offset-4">
                    <br>
                        <img class="img-responsive" src="{{ UserProfile.image.url }}">
                    <br>
                    </div>
                    {% endif %}"""),
        )
        
class PasswordResetFormCDGRD(PasswordResetForm):
    PasswordResetForm.base_fields["email"].widget.attrs.update({'class': "form-control"})

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = [
            "title",
            "fenomena",
            "descrip",
            "lat",
            "lng",
        ]
    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            "title",
            "fenomena",
            Field("descrip", rows="3"),
            "lat",
            "lng",
            )
class PhotosForm(forms.ModelForm):
    class Meta:
        model = Photos
        fields = [
            "imagedescription",
            "image",            
        ]
    def __init__(self, *args, **kwargs):
        super(PhotosForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-6'
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Field("imagedescription", rows="2"),
            "image",
            HTML("""{% if UserProfile.image.url != null %}
                    <div class="col-md-3">
                    <br>
                        <img class="img-responsive" src="{{ UserProfile.image.url }}">
                    <br>
                    </div>
                    {% endif %}"""),

        )
        self.render_required_fields = True

UploadPhotosFormset = forms.modelformset_factory(
    Photos,
    PhotosForm,
)

PhotosFormSet = forms.inlineformset_factory(
    Report,
    Photos,
    PhotosForm,
    UploadPhotosFormset,
    extra=2,
    min_num=1,
)