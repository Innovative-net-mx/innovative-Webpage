from django.db import models


# Create your models here.

class Formulario_Contacto():
    nombre = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.IntegerField(max_length=10)
    empresa = models.CharField()
    extension = models.IntegerField()
    descripcion = models.CharField()

