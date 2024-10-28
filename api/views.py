from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Email_ContactButton_Conversion
from homepage.urls import urlpatterns
import uuid
import time
from django.urls import reverse_lazy
from django.shortcuts import redirect

# Create your views here.
@csrf_exempt
def create_conversion(request):
    if request.method == 'POST':
        unique_url = str(uuid.uuid4())
        conversion = Email_ContactButton_Conversion.objects.create(unique_url=unique_url)
        return JsonResponse({'unique_url': unique_url})

def track_conversion(request, campaing_id):
    try:
        conversion = Email_ContactButton_Conversion.objects.get(campaing_id=campaing_id)
        conversion.times_clicked += 1
        conversion.datetime_last_clicked = time.strftime('%Y-%m-%d %H:%M:%S')
        conversion.save()
        return redirect('contacto')
    except Email_ContactButton_Conversion.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Invalid URL'})