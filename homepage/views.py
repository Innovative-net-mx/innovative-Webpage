from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

# Create your views here.
from .models import *
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, "homepage/home_ruben.html")

def cartera_servicios(request):
    return render(request, "homepage/carteraServicios.html")

# make a class view for a form Formulario_Contacto
class Contacto_Form(CreateView):
    model = Formulario_Contacto
    fields = ['nombre', 'email', 'phone', 'empresa', 'extension', 'descripcion']
    success_url = reverse_lazy('homepage:home')
    template_name = 'homepage/contacto.html'
