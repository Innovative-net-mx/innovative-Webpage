from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView, CreateView, DeleteView, UpdateView, TemplateView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django import forms
from .forms import *
from .models import *
from .models_hiring import Hiring_Spot, Hiring_requests
from django.http import HttpResponse
import json
import requests
import mimetypes
import base64
from django.conf import settings
# Create your views here.
class CustomLoginView(LoginView):
    # Esta clase se encarga de verificar que el usuario este autenticado antes de poder
    # entrar a cualquier parte de la pagina.
    template_name = 'CRM/login.html'
    fields = '__all__'
    form_class = PrettyAuthenticationForm
    redirect_authenticated_user = True

    # Regresa al usuario a la pagina principal si ya esta autenticado
    def get_success_url(self) -> str:
        return reverse_lazy('crm_noticias_list')

    # si el usuario no esta autenticado lo envia a la pagina de login
    def login(request):
        return render(request, "CRM/login.html")


def index(request):
    return render(request, "homepage/index.html")

def aviso_privacidad(request):
    return render(request, "homepage/aviso_privacidad.html")

def cartera_servicios(request):
    return render(request, "homepage/carteraServicios.html")

def done(request):
    return render(request, "misc/done.html")

class Objetivos(ListView):
    model = CRM_noticas
    template_name = 'homepage/objetivos.html'
    from_class = CRM_noticia_form
    context_object_name = "noticias"

    def get_queryset(self):
        return CRM_noticas.objects.order_by('-id')[:3]


class Noticia_Lista(ListView):
    model = CRM_noticas, CRM_noticas_marketing
    template_name = 'bloque/noticia.html'
    from_class = CRM_noticia_form
    context_object_name = "noticias"

def noticia_detail(request, id):
    noticia = get_object_or_404(CRM_noticas, id=id)
    noticias_sidebar = CRM_noticas.objects.order_by('-id')[:5]
    return render(request, 'CRM/noticias/noticia_detail.html', {
        'news_date': noticia.fecha,
        'news_body': noticia.descripcion,
        'news_title': noticia.titulo,
        'news_image': noticia.imagen.url if noticia.imagen else None,
        'noticias_sidebar': noticias_sidebar
    })

def noticia_mkt_detail(request, id):
    noticia = get_object_or_404(CRM_noticas_marketing, id=id)
    noticias_sidebar = CRM_noticas_marketing.objects.order_by('-id')[:5]
    return render(request, 'CRM/noticias/noticia_mkt_detail.html', {
        'news_date': noticia.fecha,
        'news_body': noticia.descripcion,
        'news_title': noticia.titulo,
        'agente': noticia.agente,
        'agente_puesto': noticia.agente_puesto,
        'agente_email': noticia.agente_email,
        'agente_img': noticia.agente_img.url if noticia.agente_img else None,
        'news_image': noticia.imagen.url if noticia.imagen else None,
        'noticias_sidebar': noticias_sidebar
    })


    
def inicio(request):
    return render(request, "homepage/index.html")

def error_form(request):
    return render(request, "homepage/error_form.html")

# make a class view for a form Formulario_Contacto

class Contacto_Form(TemplateView):
    template_name = 'homepage/contacto.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = FormularioContactoForm()
        context['form'] = form
        context['recaptcha_site_key'] = getattr(settings, 'RECAPTCHA_SITE_KEY', None)
        try:
            with open('llaves.txt') as f:
                for line in f:
                    if line.startswith("GOOGLE_MAPS_KEY="):
                        context['google_maps_api_key'] = line.strip().split("=")[1]
                        break
        except FileNotFoundError:
            context['google_maps_api_key'] = None
        return context

    def post(self, request, *args, **kwargs):
        form = FormularioContactoForm(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        secret_key = settings.RECAPTCHA_SECRET_KEY
        monday_api_key = settings.MONDAY_API_KEY
        request = self.request
        # captcha verification
        captcha_response = request.POST.get('g-recaptcha-response')
        if not captcha_response:
            messages.error(request, 'Captcha response is missing. Please try again.')
            return self.render_to_response(self.get_context_data())
        
        captcha_data = {
            'response': captcha_response,
            'secret': secret_key
        }
        
        try:
            resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captcha_data)
            resp.raise_for_status()
            result_json = resp.json()
        except requests.exceptions.RequestException as e:
            messages.error(request, f'Captcha verification failed due to a network error: {e}')
            return self.render_to_response(self.get_context_data())

        if not result_json.get('success'):
            error_codes = result_json.get('error-codes', [])
            messages.error(request, f'Captcha verification failed. Error codes: {error_codes}')
            return self.render_to_response(self.get_context_data())

        form.instance.author = request.user

        # Add Monday.com integration here
        self.create_monday_item(form.cleaned_data, monday_api_key)
        
        # Send email
        send_mail(
            'Nueva Solicitud Enviada desde la Pagina Web',
            f'Name: {form.cleaned_data["nombre"]}\nEmail: {form.cleaned_data["email"]}\nMessage: {form.cleaned_data["descripcion"]}',
            'no-reply@innovative-net.mx',
            ['desarrollo.it2@innovative-net.mx', 'hector.torres@innovative-net.mx'],
            fail_silently=False,
        )

        # Display success message
        messages.success(self.request, 'Your message has been sent!')

        return redirect(self.get_success_url())
    
    def create_monday_item(self, form_data, monday_api_key):
        url = "https://api.monday.com/v2"
        headers = {"Authorization": monday_api_key}
        query = """
            mutation ($myItemName: String!, $columnValues: JSON!) {
                create_item (board_id: 3787551203, item_name: $myItemName, column_values: $columnValues) {
                    id
                }
            }
        """
        # Define column IDs here
        column_ids = {
            "email": "email",  # Replace with actual column ID
            "phone_1": "phone_1",  # Replace with actual column ID
            "text0": "text0",
            "n_mero": "n_mero",
            "long_text": "long_text",
            # ... add other columns as necessary ...
        }

        # Prepare the column values
        column_values = {
            "email": {
                "email": str(form_data['email']),
                "text": str(form_data['email'])
            },
            "phone_1": {
                "phone": '52'+str(form_data['phone']),
                "countryShortName": "MX"  # Use the appropriate country code
            },
            "text0": form_data['empresa'],  # Assuming 'empresa' is a text column
            "n_mero": str(form_data['extension']) if form_data['extension'] else None,  # Assuming 'n_mero' is a text or number column
            "long_text": form_data['descripcion'],  # Assuming 'long_text' is a long text column
            # Add other fields as necessary
        }

        # Serialize the entire column_values dictionary
        column_values_json = json.dumps({column_ids[key]: value for key, value in column_values.items()})
        data = {
            'query': query,
            'variables': {
                'myItemName': form_data['nombre'],  # This can be any field or static text
                'columnValues': column_values_json
            }
        }
        response = requests.post(url, json=data, headers=headers)
        # Handle the response, check for errors, etc.
        if response.status_code != 200:
            print("Error in API call:", response.status_code, response.text)
        else:
            print("API call successful:", response.json())

    def get_success_url(self):
        return reverse_lazy('contacto')

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error with your form submission. Please try again.')
        return self.render_to_response(self.get_context_data())

# ========>> CRM VIEWS <<==========

# class view in wich it show the data base list of CRM_noticias
class CRM_noticias_list(LoginRequiredMixin, ListView):
    template_name = 'CRM/listado_noticias.html'
    from_class = CRM_noticia_form
    context_object_name = 'noticias'

    def get_queryset(self):
        # Combine both models' objects into a single list, ordered by id descending
        noticias = list(CRM_noticas.objects.all())
        noticias_marketing = list(CRM_noticas_marketing.objects.all())
        combined = noticias + noticias_marketing
        # Optionally, sort by id if both models have an 'id' field
        combined.sort(key=lambda x: x.id, reverse=True)
        return combined

class CRM_noticias_create(LoginRequiredMixin, CreateView):
    model = CRM_noticas
    form_class = CRM_noticia_form
    template_name = 'CRM/agregar_noticia.html'
    success_url = reverse_lazy('crm_noticias_list')

class CRM_noticias_mkt_create(LoginRequiredMixin, CreateView):
    model = CRM_noticas_marketing
    form_class = CRM_noticia_mkt_form  # Asegúrate de tener este form en tu archivo forms.py
    template_name = 'CRM/agregar_noticia_mkt.html'
    success_url = reverse_lazy('form_done')  # Cambia si quieres redirigir a otra vista

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

# ========>> BOLETIN TECNICO <<==========

from django.core.mail import EmailMessage
from django.conf import settings
from .forms import SendPDFForm
from PyPDF2 import PdfReader
from django.shortcuts import render, redirect
import re

def pdf_preview(request):
    success_message = request.session.get('success_message', None)
    form = SendPDFForm()
    if request.method == 'POST':
        form = SendPDFForm(request.POST)
        if form.is_valid():
            # Process the form data
            name = form.cleaned_data['name']
            email_user = form.cleaned_data['email']
            company = form.cleaned_data['company']

            # Send the PDF by email
            email_subject = 'Your Requested PDF'
            email_body = f"Que tal {name},\n\nEste correo contiene el bletin tecnico que requirio."
            email = EmailMessage(
                email_subject, email_body, settings.EMAIL_HOST_USER, [email_user]
            )

            # Attach PDF
            with open('homepage/static/pdf/boletin_1.pdf', 'rb') as pdf:
                email.attach('ataque-ciber-fisico.pdf', pdf.read(), 'application/pdf')

            # Send the email
            email.send()

            #### Send notification email to the company #####
            email_subject = 'Nueva Solicitud de Boletin Tecnico'
            email_body = f"Los siguientes datos fueron ingresados para obtener el boletin tecnico. \n\n Name: {name}\nEmail: {email_user}\nCompany: {company}"
            email = EmailMessage(
                email_subject, email_body, settings.EMAIL_HOST_USER, [
                    'desarrollo.it2@innovative-net.mx',
                    'hector.torres@innovative-net.mx'
                    ]
            )
            email.send()

            mydictionary = {
                "form": SendPDFForm(),
            }
            mydictionary["success"] = True
            success_message = "El boletin tecnico se ha enviado correctamente"
            request.session['success_message'] = success_message
            return redirect('ataque-ciber-fisico')
            # Redirect after POST
    # Load the PDF file
    pdf_path = 'homepage/static/pdf/boletin_1.pdf'
    reader = PdfReader(pdf_path)

    def is_header_line(index, lines_to_exclude=10):
        """
        Determine if a line is potentially part of the header.
        This function considers the first few lines of each page as potential header content.

        :param index: The index of the line on the page.
        :param lines_to_exclude: The number of lines to consider as header. Default is 3.
        :return: True if the line is potentially a header, False otherwise.
        """
        return index < lines_to_exclude

    def is_subtitle(line, next_line):
        """
        Heuristic to determine if a line is a subtitle.
        Assumes a subtitle is a shorter line followed by an empty line, in all uppercase, 
        or starts and ends with a question mark.

        :param line: The current line of text.
        :param next_line: The next line of text.
        :return: True if the line is likely a subtitle, False otherwise.
        """
        is_all_caps = line.isupper()
        starts_ends_with_question_mark = line.startswith('¿') and line.endswith('?')

        return is_all_caps or starts_ends_with_question_mark

    def is_end_of_paragraph(line):
        """
        Determine if a line is likely the end of a paragraph.
        Assumes a paragraph usually ends with a period, exclamation mark, or question mark.

        :param line: The current line of text.
        :return: True if the line is likely the end of a paragraph, False otherwise.
        """
        return line.strip().endswith(('.\n', '!', '?'))

    # Extract and handle text across pages
    all_lines = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            lines = page_text.split('\n')
            all_lines.extend([line for index, line in enumerate(lines) if not is_header_line(index)])

    paragraphs = []
    paragraph = ''
    for i, line in enumerate(all_lines):
        next_line = all_lines[i + 1] if i + 1 < len(all_lines) else ''
        if is_subtitle(line, next_line):
            if paragraph:
                paragraphs.append(paragraph.strip())
                paragraph = ''
            paragraphs.append(f"{line}")
        elif line.strip(): 
            paragraph += line + ' '
            if is_end_of_paragraph(line) or not next_line.strip():
                paragraphs.append(paragraph.strip())
                paragraph = ''
        elif not paragraph:
            # Add the last paragraph if it's not empty and no continuation is detected
            paragraphs.append(paragraph.strip())
            paragraph = ''

    # Display the first few paragraphs for review
    paragraphs = paragraphs[:10]  # Displaying the first 10 paragraphs as a sample

    context = {
        'form': form, 'pdf_content': paragraphs,
        'success_message': success_message,
        }
    
    if success_message:
        del request.session['success_message']
    return render(request, 'boletin/btec1.html', context)
