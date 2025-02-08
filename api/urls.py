from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PropertyViewSet, root_page

router = DefaultRouter()
router.register(r'properties', PropertyViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', root_page)
]
