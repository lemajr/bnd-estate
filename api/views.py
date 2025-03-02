from rest_framework import viewsets
from .models import Property
from .serializers import PropertySerializer
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Property, Visitor, Like, Booking, Subscriber, InTouchMessage
from .serializers import PropertySerializer, VisitorSerializer, LikeSerializer, BookingSerializer, SubscriberSerializer, InTouchMessageSerializer
from rest_framework.permissions import AllowAny


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
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class SubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer

class InTouchMessageViewSet(viewsets.ModelViewSet):
    queryset = InTouchMessage.objects.all()
    serializer_class = InTouchMessageSerializer


