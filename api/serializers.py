from rest_framework import serializers
from .models import Property, Visitor, Like, Booking, Subscriber, InTouchMessage
from .models import Property

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = '__all__'

class InTouchMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = InTouchMessage
        fields = '__all__'
