from django.db import models
from decouple import config

class Property(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    image_public_id = models.CharField(max_length=255, blank=True, null=True)  # Store Cloudinary public_id
    userEmail = models.EmailField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    facilities = models.JSONField(default=dict)

    def __str__(self):
        return self.title

    @property
    def image_url(self):
        if self.image_public_id:
            return f"https://res.cloudinary.com/{config('CLOUDINARY_APP_NAME')}/image/upload/{self.image_public_id}"
        return None