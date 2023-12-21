from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from .forms import *
from django.contrib import messages
from django.core.mail import send_mail

from django.views.generic.list import ListView
# Create your views here.
from .models import *
from django.http import HttpResponse
import json
import requests
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

def cartera_servicios(request):
    return render(request, "homepage/carteraServicios.html")

class Objetivos(ListView):
    model = CRM_noticas
    template_name = 'homepage/objetivos.html'
    from_class = CRM_noticia_form
    context_object_name = "noticias"

    def get_queryset(self):
        return CRM_noticas.objects.order_by('-id')[:3]


class Noticia_Lista(ListView):
    model = CRM_noticas
    template_name = 'bloque/noticia.html'
    from_class = CRM_noticia_form
    context_object_name = "noticias"

def inicio(request):
    return render(request, "homepage/index.html")

def error_form(request):
    return render(request, "homepage/error_form.html")

# make a class view for a form Formulario_Contacto
class Contacto_Form(CreateView):
    model = Formulario_Contacto
    form_class = FormularioContactoForm
    template_name = 'homepage/contacto.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        
        # Add Monday.com integration here
        self.create_monday_item(form.cleaned_data)
        
        # Send email
        send_mail(
            'Nueva Solicitud Enviada desde la Pagina Web',
            f'Name: {form.cleaned_data["nombre"]}\nEmail: {form.cleaned_data["email"]}\nMessage: {form.cleaned_data["descripcion"]}',
            'no-reply@innovative-net.mx',
            ['desarrollo.it2@innovative-net.mx',
            'hector.torres@innovative-net.mx'
            ],
            fail_silently=False,
        )

        # Display success message
        messages.success(self.request, 'Your message has been sent!')

        return super().form_valid(form)

    def create_monday_item(self, form_data):
        url = "https://api.monday.com/v2"
        headers = {"Authorization": "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjI2NTkwMzEwMSwiYWFpIjoxMSwidWlkIjoxOTI0MDkyMiwiaWFkIjoiMjAyMy0wNi0yOVQxOTo0ODowNy4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MjMzNTY1LCJyZ24iOiJ1c2UxIn0.orZN0oA-P0jWsch_XgqyES_AKqE0lQThkO8vt4o_Mas"}
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
        print(column_values)
        data = {
            'query': query,
            'variables': {
                'myItemName': form_data['nombre'],  # This can be any field or static text
                'columnValues': json.dumps(column_values)
            }
        }
        response = requests.post(url, json=data, headers=headers)
        # Handle the response, check for errors, etc.
        # Error handling
        if response.status_code != 200:
            print("Error in API call:", response.status_code, response.text)
        else:
            print("API call successful:", response.json())

    def get_success_url(self):
        return reverse_lazy('contacto')
    def get_error_url(self):
        return reverse_lazy('error_form')

# ========>> CRM VIEWS <<==========

# class view in wich it show the data base list of CRM_noticias
class CRM_noticias_list(LoginRequiredMixin, ListView):
    model = CRM_noticas
    template_name = 'CRM/listado_noticias.html'
    from_class = CRM_noticia_form
    context_object_name = 'noticias'

class CRM_noticias_create(LoginRequiredMixin, CreateView):
    model = CRM_noticas
    form_class = CRM_noticia_form
    template_name = 'CRM/agregar_noticia.html'
    success_url = reverse_lazy('crm_noticias_list')


# ========>> BOLETIN TECNICO <<==========

from django.core.mail import EmailMessage
from django.conf import settings
from .forms import SendPDFForm
from PyPDF2 import PdfReader
from django.shortcuts import render, redirect
import re

def pdf_preview(request):
    form = SendPDFForm()
    if request.method == 'POST':
        form = SendPDFForm(request.POST)
        if form.is_valid():
            # Process the form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            company = form.cleaned_data['company']

            # Send the PDF by email
            email_subject = 'Your Requested PDF'
            email_body = f"Que tal {name},\n\nEste correo contiene el bletin tecnico que requirio."
            email = EmailMessage(
                email_subject, email_body, settings.EMAIL_HOST_USER, [email]
            )

            # Attach PDF
            with open('homepage/static/pdf/boletin_1.pdf', 'rb') as pdf:
                email.attach('ataque-ciber-fisico.pdf', pdf.read(), 'application/pdf')

            # Send the email
            email.send()

            # Redirect after POST
    def get_success_url(self):
            return reverse_lazy('ataque-ciber-fisico')
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

    context = {'form': form, 'pdf_content': paragraphs}
    return render(request, 'boletin/btec1.html', context)










