from django.db import models

# Create your models here.

class Formulario_Contacto():
    nombre = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.PhoneNumberField()
    empresa = models.CharField()
    extension = models.IntegerField()
    descripcion = models.CharField()

