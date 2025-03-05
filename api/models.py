from django.db import models
from cloudinary.models import CloudinaryField
from django_countries.fields import CountryField
from django.core.exceptions import ValidationError
from cloudinary.models import CloudinaryField
import cloudinary.uploader


class Property(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=255)  
    city = models.CharField(max_length=100, blank=True, null=True)
    country = CountryField(blank_label="Select a country")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.address}, {self.city}, {self.country.name}"

    def validate_media_limits(self):
        # Fetch all related media
        media_items = self.media.all()  # We'll define this relationship in PropertyMedia
        images = media_items.filter(media_type='image')
        videos = media_items.filter(media_type='video')

        # Rule 1: Max 3 images
        if images.count() > 3:
            raise ValidationError("A property cannot have more than 3 images.")

        # Rule 2: Max 1 video
        if videos.count() > 1:
            raise ValidationError("A property cannot have more than 1 video.")

        # Rule 3: Total media (images + videos) <= 4
        if media_items.count() > 4:
            raise ValidationError("A property cannot have more than 4 media items in total.")

    def save(self, *args, **kwargs):
        # Validate media limits before saving
        super().save(*args, **kwargs)
        self.validate_media_limits()


class PropertyMedia(models.Model):
    MEDIA_TYPES = (
        ('image', 'Image'),
        ('video', 'Video'),
    )

    property = models.ForeignKey('Property', related_name='media', on_delete=models.CASCADE)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)
    file = CloudinaryField("file", blank=True, null=True, resource_type='auto')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.media_type} for {self.property.title}"

    def save(self, *args, **kwargs):
        # Ensure the file is uploaded with the correct resource type
        if self.file and not hasattr(self.file, 'public_id'):  # File is not yet uploaded to Cloudinary
            resource_type = 'image' if self.media_type == 'image' else 'video'
            try:
                # Upload the file to Cloudinary with the specified resource type
                result = cloudinary.uploader.upload(self.file, resource_type=resource_type)
                # Update the CloudinaryField with the uploaded file's public_id
                self.file = result['public_id']
            except Exception as e:
                raise ValidationError(f"Failed to upload file to Cloudinary: {str(e)}")

        super().save(*args, **kwargs)


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
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE, related_name='bookings')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='bookings')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('visitor', 'property') 
        indexes = [
            models.Index(fields=['visitor', 'property']),
        ]  

    def __str__(self):
        return f"{self.visitor.username} booked {self.property.title}"


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
