from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from .forms import *
from django.contrib import messages
from django.core.mail import send_mail

from django.views.generic.list import ListView
# Create your views here.
from .models import *
from django.http import HttpResponse
import json
import requests
# Create your views here.
class CustomLoginView(LoginView):
    # Esta clase se encarga de verificar que el usuario este autenticado antes de poder
    # entrar a cualquier parte de la pagina.
    template_name = 'CRM/login.html'
    fields = '__all__'
    form_class = PrettyAuthenticationForm
    redirect_authenticated_user = True

    # Regresa al usuario a la pagina principal si ya esta autenticado
    def get_success_url(self) -> str:
        return reverse_lazy('crm_noticias_list')

    # si el usuario no esta autenticado lo envia a la pagina de login
    def login(request):
        return render(request, "CRM/login.html")


def index(request):
    return render(request, "homepage/index.html")

def cartera_servicios(request):
    return render(request, "homepage/carteraServicios.html")

class Objetivos(ListView):
    model = CRM_noticas
    template_name = 'homepage/objetivos.html'
    from_class = CRM_noticia_form
    context_object_name = "noticias"

    def get_queryset(self):
        return CRM_noticas.objects.order_by('-id')[:3]


class Noticia_Lista(ListView):
    model = CRM_noticas
    template_name = 'bloque/noticia.html'
    from_class = CRM_noticia_form
    context_object_name = "noticias"

def inicio(request):
    return render(request, "homepage/index.html")

def error_form(request):
    return render(request, "homepage/error_form.html")

# make a class view for a form Formulario_Contacto
class Contacto_Form(CreateView):
    model = Formulario_Contacto
    form_class = FormularioContactoForm
    template_name = 'homepage/contacto.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        
        # Add Monday.com integration here
        self.create_monday_item(form.cleaned_data)
        
        # Send email
        send_mail(
            'Nueva Solicitud Enviada desde la Pagina Web',
            f'Name: {form.cleaned_data["nombre"]}\nEmail: {form.cleaned_data["email"]}\nMessage: {form.cleaned_data["descripcion"]}',
            'no-reply@innovative-net.mx',
            ['desarrollo.it2@innovative-net.mx','daniel.jara@innovative-net.mx'],
            fail_silently=False,
        )

        # Display success message
        messages.success(self.request, 'Your message has been sent!')

        return super().form_valid(form)

    def create_monday_item(self, form_data):
        url = "https://api.monday.com/v2"
        headers = {"Authorization": "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjI2NTkwMzEwMSwiYWFpIjoxMSwidWlkIjoxOTI0MDkyMiwiaWFkIjoiMjAyMy0wNi0yOVQxOTo0ODowNy4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MjMzNTY1LCJyZ24iOiJ1c2UxIn0.orZN0oA-P0jWsch_XgqyES_AKqE0lQThkO8vt4o_Mas"}
        query = """
            mutation ($myItemName: String!, $columnValues: JSON!) {
                create_item (board_id: 3787551203, item_name: $myItemName, column_values: $columnValues) {
                    id
                }
            }
        """
        # Prepare the column values as JSON
        column_values = {
            "Venderdor": form_data['nombre'],
            "Correo electronico": form_data['email'],
            "Telefono": str(form_data['phone']),
            "Compañía": form_data['empresa'],
            "Extension": str(form_data['extension']) if form_data['extension'] else None,
            # Add other fields as necessary
        }
        data = {
            'query': query,
            'variables': {
                'myItemName': form_data['nombre'],  # This can be any field or static text
                'columnValues': json.dumps(column_values)
            }
        }
        response = requests.post(url, json=data, headers=headers)
        # Handle the response, check for errors, etc.

    def get_success_url(self):
        return reverse_lazy('contacto')
    def get_error_url(self):
        return reverse_lazy('error_form')

# ========>> CRM VIEWS <<==========

# class view in wich it show the data base list of CRM_noticias
class CRM_noticias_list(LoginRequiredMixin, ListView):
    model = CRM_noticas
    template_name = 'CRM/listado_noticias.html'
    from_class = CRM_noticia_form
    context_object_name = 'noticias'

class CRM_noticias_create(LoginRequiredMixin, CreateView):
    model = CRM_noticas
    form_class = CRM_noticia_form
    template_name = 'CRM/agregar_noticia.html'
    success_url = reverse_lazy('crm_noticias_list')






