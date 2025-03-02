from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PropertyViewSet, root_page, VisitorViewSet, LikeViewSet, BookingViewSet, SubscriberViewSet, InTouchMessageViewSet

router = DefaultRouter()
router.register(r'properties', PropertyViewSet)
router.register(r'visitors', VisitorViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'subscribers', SubscriberViewSet)
router.register(r'intouchmessages', InTouchMessageViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('', root_page)
]
