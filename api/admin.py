from django.contrib import admin
from .models import Property, Visitor, Like, Booking, Subscriber, InTouchMessage
from unfold.admin import ModelAdmin
from django.contrib import admin
from django import forms
from django.utils.text import get_valid_filename
from django.core.exceptions import ValidationError
from .models import Property, PropertyMedia

# Custom form for PropertyMedia to handle file validation
class PropertyMediaForm(forms.ModelForm):
    class Meta:
        model = PropertyMedia
        fields = '__all__'

    def clean_file(self):
        file = self.cleaned_data.get('file')
        media_type = self.cleaned_data.get('media_type')

        if not file:
            return file

        # Validate file extension based on media_type
        file_name = get_valid_filename(file.name).lower()
        if media_type == 'image' and not file_name.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            raise ValidationError("File must be an image (jpg, jpeg, png, gif) for media_type 'image'.")
        if media_type == 'video' and not file_name.endswith(('.mp4', '.mov', '.avi')):
            raise ValidationError("File must be a video (mp4, mov, avi) for media_type 'video'.")

        # Optionally validate file size or other properties
        max_size = 10 * 1024 * 1024  # 10 MB limit
        if file.size > max_size:
            raise ValidationError("File size must not exceed 10 MB.")

        return file

    def clean(self):
        cleaned_data = super().clean()
        media_type = cleaned_data.get('media_type')
        file = cleaned_data.get('file')

        if not file or not media_type:
            return cleaned_data

        # Additional validation can go here if needed
        return cleaned_data

# Inline admin for PropertyMedia
class PropertyMediaInline(admin.TabularInline):
    model = PropertyMedia
    form = PropertyMediaForm
    extra = 1
    fields = ('media_type', 'file', 'uploaded_at')
    readonly_fields = ('uploaded_at',)
    can_delete = True

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('-uploaded_at')

# Custom admin for Property
@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'city', 'country', 'created_at', 'image_count', 'video_count')
    search_fields = ('title', 'city', 'country', 'address')
    list_filter = ('city', 'country', 'created_at', 'media__media_type')
    inlines = [PropertyMediaInline]

    def image_count(self, obj):
        return obj.media.filter(media_type='image').count()
    image_count.short_description = 'Images'

    def video_count(self, obj):
        return obj.media.filter(media_type='video').count()
    video_count.short_description = 'Videos'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.validate_media_limits()

@admin.register(Visitor)
class VisitorAdmin(ModelAdmin):
    list_display = ('username', 'email', 'created_at')
    search_fields = ('username', 'email')

@admin.register(Like)
class LikeAdmin(ModelAdmin):
    list_display = ('visitor', 'property', 'created_at')
    search_fields = ('visitor__username', 'property__title')

@admin.register(Booking)
class BookingAdmin(ModelAdmin):
    list_display = ('visitor', 'property', 'created_at')
    search_fields = ('visitor__username', 'property__title')

@admin.register(Subscriber)
class SubscriberAdmin(ModelAdmin):
    list_display = ('email', 'created_at')
    search_fields = ('email',)

@admin.register(InTouchMessage)
class InTouchMessageAdmin(ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')


