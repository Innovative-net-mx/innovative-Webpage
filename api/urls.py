from django.urls import path
from . import views
from homepage import views as homepage
from homepage.views import Contacto_Form
from .views import *
from django.contrib.auth.views import LogoutView
from .models import Email_ContactButton_Conversion
from django.urls import path, re_path
from django.conf.urls.static import static  # para poder mostrar imagenes
from django.conf import settings  # para poder mostrar imagenes

from django.conf.urls.static import static  # para poder mostrar imagenes
from django.conf import settings  # para poder mostrar imagenes


urlpatterns = [
    path('contact-us/', Contacto_Form.as_view(), name='contact_us'),
    path('unsubscribe/UFjb6WxujTZ1UH8e/<str:email>/', views.unsubscribe, name='unsubscribe'),
]

# Dynamically create URL patterns for each item in Email_ContactButton_Conversion to be used in the def of track_conversion(request, unique_url)
def generate_conversion_urls():
    conversion_urls = []
    for conversion in Email_ContactButton_Conversion.objects.all():
        conversion_urls.append(
            path(f'track-conversion/{conversion.campaing_id}/', views.track_conversion, {'campaing_id': conversion.campaing_id}, name=f'track_conversion_{conversion.campaing_id}')
        )
    return conversion_urls

urlpatterns += generate_conversion_urls()

# URL pattern for unsubscribe button click

