from django.urls import path
from . import views
from .views import Contacto_Form
urlpatterns = [ 
    path("", views.index, name="index"),
    path("cartera_servicios", views.cartera_servicios, name="cartera_servicios"),
    path("contacto", Contacto_Form.as_view(), name="contacto"),
]