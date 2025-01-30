from django.contrib import admin
from .models import Property

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('title', 'city', 'country', 'price', 'userEmail', 'createdAt', 'updatedAt')
    
    # Fields to filter by in the right sidebar
    list_filter = ('city', 'country', 'createdAt')
    
    # Fields to search by in the search bar
    search_fields = ('title', 'city', 'country', 'userEmail')
    
    # Fields to allow editing directly in the list view
    list_editable = ('price',)
    
    # Fields to group in the edit form
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'price', 'userEmail')
        }),
        ('Location', {
            'fields': ('address', 'city', 'country', 'latitude', 'longitude')
        }),
        ('Image', {
            'fields': ('image_public_id',)
        }),
        ('Facilities', {
            'fields': ('facilities',)
        }),
        ('Timestamps', {
            'fields': ('createdAt', 'updatedAt'),
            'classes': ('collapse',)  # Collapsible section
        }),
    )
    
    # Read-only fields
    readonly_fields = ('createdAt', 'updatedAt', 'image_url')
    
    # Custom method to display the image URL
    def image_url(self, obj):
        return obj.image_url
    image_url.short_description = 'Image URL'  # Column header in the admin