from django import forms
from .models import Formulario_Contacto


class FormularioContactoForm(forms.ModelForm):
    class Meta:
        model = Formulario_Contacto
        fields = ['nombre', 'email', 'phone',
                  'empresa', 'extension', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'contact-from'}),
            'email': forms.EmailInput(attrs={'class': 'contact-from''}),
            'phone': forms.NumberInput(attrs={'class': 'contact-from-phone'}),
            'empresa': forms.TextInput(attrs={'class': 'contact-from'}),
            'extension': forms.NumberInput(attrs={'class': 'contact-from-extension''}),
            'descripcion': forms.TextInput(attrs={'class': 'contact-from-descripcion'}),
        }
