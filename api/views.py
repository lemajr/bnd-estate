from rest_framework import viewsets
from .models import Property
from .serializers import PropertySerializer
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Property, Visitor, Like, Booking, Subscriber, InTouchMessage
from .serializers import PropertySerializer, VisitorSerializer, LikeSerializer, BookingSerializer, SubscriberSerializer, InTouchMessageSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
def root_page(request):
    return HttpResponse(
        """
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Property API</title>
            <style>
                body {
                    font-family: 'Arial', sans-serif;
                    background-color: #f4f7f6;
                    color: #333;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }
                .container {
                    background-color: white;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                    width: 80%;
                    max-width: 600px;
                    padding: 20px;
                    text-align: center;
                }
                h1 {
                    color: #4CAF50;
                    font-size: 36px;
                    margin-bottom: 20px;
                }
                p {
                    font-size: 18px;
                    color: #666;
                    margin-bottom: 20px;
                }
                ul {
                    list-style-type: none;
                    padding: 0;
                    text-align: left;
                }
                ul li {
                    margin: 10px 0;
                }
                a {
                    color: #1e90ff;
                    text-decoration: none;
                    font-size: 18px;
                    transition: color 0.3s;
                }
                a:hover {
                    color: #333;
                    text-decoration: underline;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Welcome to the Property API</h1>
                <p>Here are the available API endpoints:</p>
                <ul>
                    <li><a href="/api/">View the API root</a></li>
                    <li><a href="/api/properties/">List all properties</a></li>
                    <li><a href="/api/properties/create/">Create a new property</a></li>
                </ul>
            </div>
        </body>
        </html>
        """
    )



class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

class VisitorViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]  

    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer

class LikeViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]  
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def list(self, request, *args, **kwargs):
        """GET /api/likes/ - Not intended for status checks, use /status/ instead"""
        visitor_id = request.query_params.get('visitor')
        property_id = request.query_params.get('property')

        if visitor_id and property_id:
            # Redirect to status action for consistency
            return self.status(request)
        else:
            # Default list behavior (optional, or disable)
            return Response(
                {'error': 'Use /api/likes/status/ with visitor and property IDs'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'])
    def status(self, request):
        """GET /api/likes/status/?visitor=<id>&property=<id>"""
        visitor_id = request.query_params.get('visitor')
        property_id = request.query_params.get('property')

        if not visitor_id or not property_id:
            return Response(
                {'error': 'Visitor and property IDs are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            is_liked = Like.objects.filter(
                visitor__id=visitor_id,
                property__id=property_id
            ).exists()
            print(f"Checked like: visitor={visitor_id}, property={property_id}, result={is_liked}")
            return Response(is_liked, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error checking like: {e}")
            return Response(
                {'error': 'Something went wrong'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def create(self, request, *args, **kwargs):
        """POST /api/likes/"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if Like.objects.filter(
            visitor__id=request.data['visitor'],
            property__id=request.data['property']
        ).exists():
            return Response({'error': 'Like already exists'}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['delete'])
    def unlike(self, request):
        """DELETE /api/likes/unlike/"""
        visitor_id = request.data.get('visitor')
        property_id = request.data.get('property')
        try:
            like = Like.objects.get(visitor__id=visitor_id, property__id=property_id)
            like.delete()
            return Response({'success': True}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({'error': 'Like not found'}, status=status.HTTP_404_NOT_FOUND)
    def create(self, request, *args, **kwargs):
        """POST /api/likes/ to create a like"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Check if like already exists
        if Like.objects.filter(
            visitor__id=request.data['visitor'],
            property__id=request.data['property']
        ).exists():
            return Response(
                {'error': 'Like already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        self.perform_create(serializer)
        return Response(
            {'success': True, 'data': serializer.data},
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=['delete'])
    def unlike(self, request):
        """DELETE /api/likes/unlike/ with visitor/property in body"""
        visitor_id = request.data.get('visitor')
        property_id = request.data.get('property')

        if not visitor_id or not property_id:
            return Response(
                {'error': 'Visitor and property IDs are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            like = Like.objects.get(visitor__id=visitor_id, property__id=property_id)
            like.delete()
            return Response({'success': True}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response(
                {'error': 'Like not found'},
                status=status.HTTP_404_NOT_FOUND
            )

class BookingViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class SubscriberViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]  

    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer

class InTouchMessageViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = InTouchMessage.objects.all()
    serializer_class = InTouchMessageSerializer


