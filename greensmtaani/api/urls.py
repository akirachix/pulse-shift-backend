from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomerViewSet, MamaMbogaViewSet, AddressViewSet,
    OrdersViewSet, Order_itemsViewSet,
    DietaryPreferenceViewSet, MealPlanViewSet
)

router = DefaultRouter()
router.register(r"customers", CustomerViewSet, basename='customers')
router.register(r"mama-mbogas", MamaMbogaViewSet, basename='mama-mbogas')
router.register(r"addresses", AddressViewSet, basename='addresses')
router.register(r"orders", OrdersViewSet, basename='orders')
router.register(r"order-items", Order_itemsViewSet, basename='order-items')
router.register(r"dietary-preferences", DietaryPreferenceViewSet, basename='dietary-preferences')
router.register(r"meal-plans", MealPlanViewSet, basename='meal-plans')

urlpatterns = [
    path('', include(router.urls)),
]