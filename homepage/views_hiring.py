from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DeleteView, UpdateView, TemplateView, ListView
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
# Create your views here.
from .models_hiring import Hiring_Spot, Hiring_requests
from .forms import SendHiringRequest
from django.http import HttpResponse
import json
import requests
from django import forms
import mimetypes
import base64
from django.conf import settings
class Main_HiringPage(TemplateView):
    template_name = 'hiring/hiring_main.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hiring'] = Hiring_Spot.objects.all()
        context['form_class'] = SendHiringRequest()
        context['form'] = SendHiringRequest()
        context['recaptcha_site_key'] = settings.RECAPTCHA_SITE_KEY
        return context

    def post(self, request, *args, **kwargs):
        """
        Guarda el formulario de la solicitude de empleo en la 
        base de datos y envia un correo con los detalles del formulario.
        """
        form = SendHiringRequest(request.POST, request.FILES)

        if form.is_valid():
            secret_key = settings.RECAPTCHA_SECRET_KEY
            monday_api_key = settings.MONDAY_API_KEY
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

            print(result_json)

            if not result_json.get('success'):
                error_codes = result_json.get('error-codes', [])
                messages.error(request, f'Captcha verification failed. Error codes: {error_codes}')
                return self.render_to_response(self.get_context_data())
            # end captcha verification
            
            hiring_request = form.save(commit=False)
            messages.success(request, 'Tus datos fueron enviados de manera exitosa.')
            print('Formulario enviado')
            
            # Check if the uploaded file name already exists
            file = hiring_request.cv
            file_name = file.name
            file_extension = file_name.split('.')[-1]
            file_base_name = '.'.join(file_name.split('.')[:-1])
            counter = 1
            while Hiring_requests.objects.filter(cv=file.name).exists():
                file.name = f"{file_base_name}_{counter}.{file_extension}"
                counter += 1
            print("passed the while loop")
            hiring_request.save()
            file_content = hiring_request.cv.read()
            hiring_request.cv.seek(0)  # Reset file pointer to the beginning
            # Send email with the details of the post and attach the file
            subject = 'New Hiring Request Submitted'
            message = f'A new hiring request has been submitted:\n\n{hiring_request}'
            from_email = 'no-reply@innovative-net.mx'
            recipient_list = ['desarrollo.it2@innovative-net.mx']
            
            # Create the email
            email = EmailMessage(subject, message, from_email, recipient_list)
            
            # Attach the file
            content_type, _ = mimetypes.guess_type(file.name)
            email.attach(hiring_request.cv.name, file_content, content_type)
            
            # Send the emails
            email.send(fail_silently=False)
            
            # Sends data to a monday.com board using the API
            url = "https://api.monday.com/v2"
            headers = {
                "Authorization": monday_api_key,
            }
            query = """
            mutation ($itemName: String!, $columnValues: JSON!) {
                create_item (board_id: 7585964077, item_name: $itemName, column_values: $columnValues) {
                    id
                }
            }
            """
            phone = str(hiring_request.phone) if str(hiring_request.phone).startswith("+52") else "+52" + str(hiring_request.phone)
            print(f"Sending data to monday.com: {form.cleaned_data} \n phone: {phone} \n category: {hiring_request.hiring_spot.category.name} \n hiring_spot: {hiring_request.hiring_spot.name} \n email: {hiring_request.email} \n cv path: {hiring_request.cv} \n \n")
            
            # Retrieve the saved hiring request to get the CV path
            saved_hiring_request = Hiring_requests.objects.get(pk=hiring_request.pk)
            cv_path = saved_hiring_request.cv.path
            with open(cv_path, "rb") as file:
                file_content = file.read()
            
            # First, create the item in monday.com
            variables = {
                "itemName": hiring_request.name,
                "columnValues": json.dumps({
                    "email__1": {"email": hiring_request.email, "text": hiring_request.email},
                    "phone__1": phone,
                    "departamento__1": hiring_request.hiring_spot.category.name,
                    "puesto0__1": hiring_request.hiring_spot.name,  # Assuming hiring_spot is a ForeignKey
                })
            }

            data = {
                "query": query,
                "variables": variables
            }
            try:
                response = requests.post(url, headers=headers, json=data)
                response.raise_for_status()  # Raise an HTTPError for bad responses
                response_data = response.json()
                if 'errors' in response_data:
                    print(f"Failed to send data to monday.com: {response_data}")
                else:
                    print(f"Successfully created item in monday.com: {response_data}")
                    item_id = response_data['data']['create_item']['id']
                    
                    # Now, upload the file to the created item
                    file_url = "https://api.monday.com/v2/file"
                    file_headers = {
                        "Authorization": headers["Authorization"],
                    }
                    file_data = {
                        "query": "mutation ($file: File!) { add_file_to_column (file: $file, item_id: " + item_id + ", column_id: \"file__1\") { id } }",
                        "variables": {}
                    }
                    files = {
                        'variables[file]': (file.name, file_content, mimetypes.guess_type(file.name)[0])
                    }
                    file_response = requests.post(file_url, headers=file_headers, data=file_data, files=files)
                    file_response.raise_for_status()
                    print(f"Successfully uploaded file to monday.com: {file_response.json()}")
            except requests.exceptions.HTTPError as http_err:
                print(f"HTTP error occurred: {http_err}")
                print(f"Response content: {response.content}")
                print(f"Request data: {json.dumps(data, indent=4)}")
                print(f"Request headers: {headers}")
            except requests.exceptions.RequestException as req_err:
                print(f"Request error occurred: {req_err}")
                print(f"Response content: {response.content}")
                print(f"Request data: {json.dumps(data, indent=4)}")
                print(f"Request headers: {headers}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                print(f"Response content: {response.content if response else 'No response'}")
                print(f"Request data: {json.dumps(data, indent=4)}")
                print(f"Request headers: {headers}")

            return redirect('bolsa-de-empleo')
        else:
            context = self.get_context_data()
            print(f'\n Error:Formulario no enviado - {form.errors} \n')
            context['form'] = form
            return self.render_to_response(context)

