from django.contrib import admin
from .models import Email_ContactButton_Conversion, Unsubscribe
# Register your models here.
class EmailContactButtonConversionAdmin(admin.ModelAdmin):
    list_display = ('campaing_name','campaing_id')

class UnsubscribeAdmin(admin.ModelAdmin):
    list_display = ('email','date_submitted')

admin.site.register(Email_ContactButton_Conversion, EmailContactButtonConversionAdmin)
admin.site.register(Unsubscribe, UnsubscribeAdmin)
