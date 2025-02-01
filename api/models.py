from django.db import models
from cloudinary.models import CloudinaryField
from django_countries.fields import CountryField

class Property(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=255)  
    city = models.CharField(max_length=100, blank=True, null=True)
    country = CountryField(blank_label="Select a country")
    image = CloudinaryField("image", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.address}, {self.city}, {self.country.name}"
