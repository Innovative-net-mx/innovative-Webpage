from django.contrib import admin
from .models import Email_ContactButton_Conversion
# Register your models here.
class EmailContactButtonConversionAdmin(admin.ModelAdmin):
    list_display = ('campaing_name','campaing_id')

admin.site.register(Email_ContactButton_Conversion, EmailContactButtonConversionAdmin)
