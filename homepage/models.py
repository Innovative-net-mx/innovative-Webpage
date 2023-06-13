from django.db import models



# Create your models here.

class Formulario_Contacto(models.Model):
    nombre = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.IntegerField()
    empresa = models.CharField(max_length=50)
    extension = models.IntegerField()
    descripcion = models.CharField(max_length=200)

