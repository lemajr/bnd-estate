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

class Visitor(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Like(models.Model):
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, related_name='likes')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('visitor', 'property')
        indexes = [models.Index(fields=['visitor', 'property'])]

    def __str__(self):
        return f"{self.visitor.username} liked {self.property.title}"

class Booking(models.Model):
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    booking_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.visitor.username} booked {self.property.title} on {self.booking_date}"

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class InTouchMessage(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.first_name} {self.last_name}"
