from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, AddressViewSet, MamaMbogaViewSet, Order_itemsViewSet, OrdersViewSet, TransactionViewSet

router = DefaultRouter()
router.register(r"customers", CustomerViewSet, basename='customers')
router.register(r"mama-mbogas", MamaMbogaViewSet, basename='mama-mbogas')
router.register(r"addresses", AddressViewSet, basename='addresses')
router.register(r"orders",OrdersViewSet, basename='orders')
router.register(r"order_items",Order_itemsViewSet, basename='order_items')
router.register(r"Transaction",TransactionViewSet, basename='transaction')


urlpatterns = [
    path('', include(router.urls))
]