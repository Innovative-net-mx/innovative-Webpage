from django.db import models



# Create your models here.

class Formulario_Contacto(models.Model):
    nombre = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.IntegerField(max_length=11)
    empresa = models.CharField(max_length=60)
    extension = models.IntegerField(blank=True, null=True, max_length=5)
    descripcion = models.CharField(max_length=200)

