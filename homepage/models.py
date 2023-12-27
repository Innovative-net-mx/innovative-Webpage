from django.db import models
from multiselectfield import MultiSelectField
from PIL import Image



# Create your models here.

class Formulario_Contacto(models.Model):
    INTENCION_LISTA = (
    ('1', 'Explorando y deseo conocer mas sobre una posible solución'), 
    ('2', 'Se lo que quiero y deseo apoyo de sus servicios y cotización.'), 
    ('3', 'Necesito un equipo Demo de su solución, necesito agendarlo con ustedes.')
    )
    nombre = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.IntegerField()
    empresa = models.CharField(max_length=60)
    extension = models.IntegerField(blank=True, null=True)
    intencion = models.CharField(max_length=1, choices=INTENCION_LISTA)
    descripcion = models.CharField(max_length=200)

class CRM_noticas(models.Model):
    titulo = models.CharField(max_length=250)
    descripcion = models.CharField(max_length=2500)
    fecha = models.DateField(auto_now_add=True)
    imagen = models.ImageField(upload_to='noticias', null=True, blank=True, default='noticia.jpg')