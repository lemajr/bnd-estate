from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Property
from .serializers import PropertySerializer
import cloudinary.uploader

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    def create(self, request, *args, **kwargs):
        # Handle image upload
        image_file = request.FILES.get('image')
        if image_file:
            try:
                upload_result = cloudinary.uploader.upload(image_file)
                request.data['image_public_id'] = upload_result['public_id']
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # Handle image update
        image_file = request.FILES.get('image')
        if image_file:
            try:
                # Delete the old image from Cloudinary
                instance = self.get_object()
                if instance.image_public_id:
                    cloudinary.uploader.destroy(instance.image_public_id)

                # Upload the new image
                upload_result = cloudinary.uploader.upload(image_file)
                request.data['image_public_id'] = upload_result['public_id']
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Delete the image from Cloudinary when the property is deleted
        instance = self.get_object()
        if instance.image_public_id:
            cloudinary.uploader.destroy(instance.image_public_id)
        return super().destroy(request, *args, **kwargs)