from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    OrdersViewSet, Order_itemsViewSet

)
router = DefaultRouter()

router.register(r"orders", OrdersViewSet, basename='orders')
router.register(r"order-items", Order_itemsViewSet, basename='order-items')


urlpatterns = [
    path('', include(router.urls)),
]