from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.urls import reverse_lazy

# Create your views here.
from .models import *
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, "homepage/index.html")

def cartera_servicios(request):
    return render(request, "homepage/cartera_servicios.html")

# make a class view for a form Formulario_Contacto
class Contacto_View(FormView):
    template_name = 'homepage/contacto.html'
    form_class = Formulario_Contacto
    success_url = reverse_lazy('homepage:contacto')

    def form_valid(self, form):
        form.save()
        return super(Contacto_View, self).form_valid(form)
