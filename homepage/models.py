from django.db import models
from PIL import Image



# Create your models here.

class Formulario_Contacto(models.Model):
    nombre = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.IntegerField(max_length=11)
    empresa = models.CharField(max_length=60)
    extension = models.IntegerField(blank=True, null=True, max_length=5)
    descripcion = models.CharField(max_length=200)

class CRM_noticas(models.Model):
    titulo = models.CharField(max_length=250)
    descripcion = models.CharField(max_length=2500)
    fecha = models.DateField(auto_now_add=True)
    imagen = models.ImageField(upload_to='noticias', null=True, blank=True, default='noticia.jpg')