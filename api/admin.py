from django.contrib import admin
from .models import Property
from unfold.admin import ModelAdmin


@admin.register(Property)
class PropertyAdmin(ModelAdmin):
    list_display = ('title', 'price', 'city', 'country', 'created_at')
    search_fields = ('title', 'city', 'country', 'user_email')




