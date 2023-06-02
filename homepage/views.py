from django.shortcuts import render, redirect

# Create your views here.
from .models import *
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, "homepage/index.html")

def template(request):
    return render(request, "homepage/template.html")

#form model view for contact form
def contact(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        empresa = request.POST.get('empresa')
        extension = request.POST.get('extension')
        descripcion = request.POST.get('descripcion')
        contact = Formulario_Contacto(nombre=nombre, email=email, phone=phone, empresa=empresa, extension=extension, descripcion=descripcion)
        contact.save()
        return redirect('index')
    return render(request, "homepage/index.html")