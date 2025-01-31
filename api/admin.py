from django.contrib import admin
from .models import Property

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'city', 'country', 'address', 'created_at')
    search_fields = ('title', 'city', 'country', 'user_email')
