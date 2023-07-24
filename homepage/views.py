from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from .forms import *
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
# Create your views here.
from .models import *
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, "homepage/home_ruben.html")

def cartera_servicios(request):
    return render(request, "homepage/carteraServicios.html")
def  objetivos(request):
    return render(request, "homepage/objetivos.html")

class Noticia_Lista(ListView):
    model = CRM_noticas
    template_name = 'bloque/noticia.html'
    from_class = CRM_noticia_form
    context_object_name = "noticias"

def inicio(request):
    return render(request, "homepage/home_ruben.html")

def error_form(request):
    return render(request, "homepage/error_form.html")

# make a class view for a form Formulario_Contacto
class Contacto_Form(CreateView):
    model = Formulario_Contacto
    form_class = FormularioContactoForm
    template_name = 'homepage/contacto.html'

    def form_valid(self, form):
        form.instance.author = self.request.user

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

    def get_success_url(self):
        return reverse_lazy('contacto')
    def get_error_url(self):
        return reverse_lazy('error_form')

# ========>> CRM VIEWS <<==========


class CustomLoginView(LoginView):
    # Esta clase se encarga de verificar que el usuario este autenticado antes de poder
    # entrar a cualquier parte de la pagina.
    template_name = 'CRM/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self) -> str:
        return reverse_lazy('')

def login(request):
    return render(request, "CRM/login.html")
# class view in wich it show the data base list of CRM_noticias
class CRM_noticias_list(ListView):
    model = CRM_noticas
    template_name = 'CRM/listado_noticias.html'
    from_class = CRM_noticia_form
    context_object_name = 'noticias'

class CRM_noticias_create(CreateView):
    model = CRM_noticas
    form_class = CRM_noticia_form
    template_name = 'CRM/agregar_noticia.html'
    success_url = reverse_lazy('crm_noticias_list')

