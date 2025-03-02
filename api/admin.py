from django.contrib import admin
from .models import Property, Visitor, Like, Booking, Subscriber, InTouchMessage
from unfold.admin import ModelAdmin


@admin.register(Property)
class PropertyAdmin(ModelAdmin):
    list_display = ('title', 'price', 'city', 'country', 'created_at')
    search_fields = ('title', 'city', 'country', 'address')

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
    list_display = ('visitor', 'property', 'booking_date', 'created_at')
    search_fields = ('visitor__username', 'property__title')

@admin.register(Subscriber)
class SubscriberAdmin(ModelAdmin):
    list_display = ('email', 'created_at')
    search_fields = ('email',)

@admin.register(InTouchMessage)
class InTouchMessageAdmin(ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')


