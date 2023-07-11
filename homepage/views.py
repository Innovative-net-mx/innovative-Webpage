from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from .forms import *
from django.contrib import messages
from django.core.mail import send_mail

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
def inicio(request):
    return render(request, "homepage/home_ruben.html")

# make a class view for a form Formulario_Contacto
class Contacto_Form(CreateView):
    model = Formulario_Contacto
    form_class = FormularioContactoForm
    template_name = 'homepage/contacto.html'

    def form_valid(self, form):
        form.instance.author = self.request.user

        # Send email
        send_mail(
            'Contact Form Submission',
            f'Name: {form.cleaned_data["nombre"]}\nEmail: {form.cleaned_data["email"]}\nMessage: {form.cleaned_data["descripcion"]}',
            'no-reply@innovative-net.mx',
            ['desarrollo.it2@innovative-net.mx','daniel.jara@innovative-net.mx'],
            fail_silently=False,
            subject=f"Nueva solicitud de contacto",
        )

        # Display success message
        messages.success(self.request, 'Your message has been sent!')

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('index')
