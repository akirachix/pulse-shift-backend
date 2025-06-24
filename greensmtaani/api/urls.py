from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, AddressViewSet, MamaMbogaViewSet

router = DefaultRouter()
router.register(r"customers", CustomerViewSet, basename='customers')
router.register(r"mama-mbogas", CustomerViewSet, basename='mama-mbogas')
router.register(r"addresses", CustomerViewSet, basename='addresses')


urlpatterns = [
    path('', include(router.urls))
]