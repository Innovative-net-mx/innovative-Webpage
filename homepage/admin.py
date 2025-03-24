from django.contrib import admin
from .models import *
from .models_hiring import Hiring_Spot, Category, Hiring_requests

admin.site.register(Formulario_Contacto)

admin.site.register(Hiring_Spot)
admin.site.register(Category)
admin.site.register(Hiring_requests)
admin.site.register(CRM_noticas)
admin.site.register(CRM_noticas_marketing)


# Register your models here.
