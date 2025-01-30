from rest_framework import serializers
from .models import Property

class PropertySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()  # Add this field to return the full image URL

    class Meta:
        model = Property
        fields = '__all__'

    def get_image_url(self, obj):
        return obj.image_url