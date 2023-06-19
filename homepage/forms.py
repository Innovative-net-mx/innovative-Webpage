from django import forms
from .models import Formulario_Contacto


class FormularioContactoForm(forms.ModelForm):
    class Meta:
        model = Formulario_Contacto
        fields = ['nombre', 'email', 'phone',
                  'empresa', 'extension', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'contact-from',
                                                   'placeholder': 'Nombre'}),
            'email': forms.EmailInput(attrs={'class': 'contact-from',
                                                   'placeholder': 'Correo electrónico'}),
            'phone': forms.NumberInput(attrs={'class': 'contact-from-phone',
                                                   'placeholder': 'Teléfono'}),
            'empresa': forms.TextInput(attrs={'class': 'contact-from',
                                                   'placeholder': 'Empresa'}),
            'extension': forms.NumberInput(attrs={'class': 'contact-from-extension',
                                                   'placeholder': 'Extensión'}),
            'descripcion': forms.TextInput(attrs={'class': 'contact-from-descripcion',
                                                   'placeholder': 'Descripción' }),
        }
