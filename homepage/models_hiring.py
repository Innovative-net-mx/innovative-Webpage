from django.db import models
from multiselectfield import MultiSelectField
from PIL import Image

class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Hiring_Spot(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Hiring_requests(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    hiring_spot = models.ForeignKey(Hiring_Spot, on_delete=models.CASCADE)
    send_date = models.DateField(auto_now_add=True)
    cv = models.FileField(upload_to='cv', null=False, blank=False) 


    def __str__(self):
        return self.name

    

    