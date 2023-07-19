from django.urls import path
from . import views
from .views import CRM_noticias_list, Contacto_Form, CRM_noticias_create

urlpatterns = [ 
    path("", views.index, name="index"),
    path("cartera_servicios", views.cartera_servicios, name="cartera_servicios"),
    path("contacto", Contacto_Form.as_view(), name="contacto"),
    path("objetivos", views.objetivos, name="objetivos" ),
    path("inicio",   views.inicio, name="inicio"),
    path("error_form", views.error_form, name="error_form"),
    path("crm_noticias_list", CRM_noticias_list.as_view(), name="crm_noticias_list"),
    path("crm_noticias_create", CRM_noticias_create.as_view(), name="crm_noticias_create"),
    path("login", views.login, name="login"),
    
]