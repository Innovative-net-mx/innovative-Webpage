from django.db import models
import uuid

# Create your models here.

class Email_ContactButton_Conversion(models.Model):
    campaing_name = models.CharField(max_length=100)
    date_submitted = models.DateTimeField(auto_now_add=True)
    times_clicked = models.IntegerField(default=0)
    datetime_last_clicked = models.DateTimeField(auto_now_add=True)
    campaing_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

class Unsubscribe(models.Model):
    email = models.EmailField(max_length=100)
    date_submitted = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email