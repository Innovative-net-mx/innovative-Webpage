from django import forms
from .models import Formulario_Contacto, CRM_noticas
from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


class FormularioContactoForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(attrs={'class': 'recaptcha-class'}))

    class Meta:
        model = Formulario_Contacto
        fields = ['nombre', 'email', 'phone', 'empresa', 'extension', 'intencion', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'contact-from'}),
            'email': forms.EmailInput(attrs={'class': 'contact-from'}),
            'phone': forms.NumberInput(attrs={'class': 'contact-from-phone'}),
            'empresa': forms.TextInput(attrs={'class': 'contact-from'}),
            'extension': forms.NumberInput(attrs={'class': 'contact-from-extension'}),
            'intencion': forms.Select(attrs={'class': 'contact-from-intencion'}),
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
