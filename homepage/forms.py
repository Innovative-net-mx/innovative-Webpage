from django import forms
from .models import Formulario_Contacto, CRM_noticas
from .models_hiring import Hiring_requests
from .models_hiring import *
from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


class FormularioContactoForm(forms.ModelForm):

    class Meta:
        model = Formulario_Contacto
        fields = ['nombre', 'email', 'phone', 'empresa', 'extension', 'intencion', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'contact-from'}),
            'email': forms.EmailInput(attrs={'class': 'contact-from'}),
            'phone': forms.NumberInput(attrs={'class': 'contact-from-phone'}),
            'empresa': forms.TextInput(attrs={'class': 'contact-from'}),
            'extension': forms.NumberInput(attrs={'class': 'contact-from-extension'}),
            'intencion': forms.Select(attrs={'class': 'contact-from-intencion', 'id': 'intencion'}),
            'descripcion': forms.Textarea(attrs={'class': 'contact-from-descripcion'})

        }

class CRM_noticia_form(forms.ModelForm):
    class Meta:
        model = CRM_noticas
        fields = ['titulo', 'descripcion', 'imagen']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'crm-noticia-titulo'}),
            'descripcion': forms.Textarea(attrs={'class': 'crm-noticia-descripcion'}),
            'imagen': forms.FileInput(attrs={'class': 'crm-noticia-imagen'})
        }

class PrettyAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'id': 'inputemail'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'inputpassword'}))


class SendPDFForm(forms.Form):
    name = forms.CharField(label='Nombre', max_length=100)
    email = forms.EmailField(label='Correo')
    company = forms.CharField(label='Compañia', max_length=100)

class SendHiringRequest(forms.ModelForm):
    class Meta:
        model = Hiring_requests
        fields = ['name', 'email', 'phone', 'description', 'hiring_spot', 'cv']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'hiring-request'}),
            'email': forms.EmailInput(attrs={'class': 'hiring-request'}),
            'phone': forms.NumberInput(attrs={'class': 'hiring-request'}),
            'description': forms.Textarea(attrs={'class': 'hiring-request'}),
            'hiring_spot': forms.Select(attrs={'class': 'hiring-request'}),
            'cv': forms.FileInput(attrs={'class': 'hiring-request', 'id': 'cv-filename', 'onchange': 'showFileName()'})
        }
