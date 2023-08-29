from django.urls import path
from . import views
from .views import *
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static  # para poder mostrar imagenes
from django.conf import settings  # para poder mostrar imagenes
urlpatterns = [ 
    path("", views.index, name="index"),
    path("cartera_servicios", views.cartera_servicios, name="cartera_servicios"),
    path("contacto", Contacto_Form.as_view(), name="contacto"),
    path("objetivos", Objetivos.as_view(), name="objetivos" ),
    path("inicio",   views.inicio, name="inicio"),
    path("error_form", views.error_form, name="error_form"),
    path("crm_noticias_list", CRM_noticias_list.as_view(), name="crm_noticias_list"),
    path("crm_noticias_create", CRM_noticias_create.as_view(), name="crm_noticias_create"),
    path("login", CustomLoginView.as_view() , name="login"),
    path("logout/", LogoutView.as_view(next_page='login'), name='logout'),
    path("noticia_bloque", Noticia_Lista.as_view(), name="noticia_bloque" )
    
]

# para poder mostrar imagenes
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)