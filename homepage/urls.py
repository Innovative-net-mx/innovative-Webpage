from django.urls import path
from . import views, views_hiring
from .views import *
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static  # para poder mostrar imagenes
from django.conf import settings  # para poder mostrar imagenes
from django.urls import include
urlpatterns = [ 
    path("", views.index, name="index"),
    path("cartera_servicios", views.cartera_servicios, name="cartera_servicios"),
    path("contacto", Contacto_Form.as_view(), name="contacto"),
    path("objetivos", Objetivos.as_view(), name="objetivos" ),
    path("inicio",   views.inicio, name="inicio"),
    path("aviso_privacidad", views.aviso_privacidad, name="aviso_privacidad"),
    path("error_form", views.error_form, name="error_form"),
    path("crm_noticias_list", CRM_noticias_list.as_view(), name="crm_noticias_list"),
    path("crm_noticias_create", CRM_noticias_create.as_view(), name="crm_noticias_create"),
    path("login", CustomLoginView.as_view() , name="login"),
    path("logout/", LogoutView.as_view(next_page='login'), name='logout'),
    path("noticia_bloque", Noticia_Lista.as_view(), name="noticia_bloque" ),
    path('ataque-ciber-fisico', views.pdf_preview, name='ataque-ciber-fisico'),
    path('bolsa-de-empleo', views_hiring.Main_HiringPage.as_view(), name='bolsa-de-empleo'),
    path('noticia/<int:id>/', noticia_detail, name='noticia_detail'),
    path('noticiamkt/<int:id>/', noticia_mkt_detail, name='noticia_mkt_detail'),
    path('noticia/create', CRM_noticias_mkt_create.as_view(), name='noticia_create'),
    path('ckeditor5/', include('django_ckeditor_5.urls'), name='mkadd'),
    path('formdone', views.done, name='form_done'),
    
]

# para poder mostrar imagenes
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)