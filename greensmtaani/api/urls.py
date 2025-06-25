from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomerViewSet, MamaMbogaViewSet, AddressViewSet,

)
router = DefaultRouter()
router.register(r"customers", CustomerViewSet, basename='customers')
router.register(r"mama-mbogas", MamaMbogaViewSet, basename='mama-mbogas')
router.register(r"addresses", AddressViewSet, basename='addresses')

urlpatterns = [
    path('', include(router.urls)),
]