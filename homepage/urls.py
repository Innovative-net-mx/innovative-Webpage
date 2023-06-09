from django.urls import path
from . import views
from .views import Contacto_View
urlpatterns = [ 
    path("", views.index, name="index"),
    path("cartera_servicios", views.cartera_servicios, name="cartera_servicios"),
    path("contacto", views.Contacto_View.as_view(), name="contacto"),
]