from django import forms
from .models import Formulario_Contacto, CRM_noticas
from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


class FormularioContactoForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(attrs={'class': 'recaptcha-class'}))

    class Meta:
        model = Formulario_Contacto
        fields = ['nombre', 'email', 'phone', 'empresa', 'extension', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'contact-from'}),
            'email': forms.EmailInput(attrs={'class': 'contact-from'}),
            'phone': forms.NumberInput(attrs={'class': 'contact-from-phone'}),
            'empresa': forms.TextInput(attrs={'class': 'contact-from'}),
            'extension': forms.NumberInput(attrs={'class': 'contact-from-extension'}),
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