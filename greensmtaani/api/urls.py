from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    OrdersViewSet, Order_itemsViewSet, ProductViewSet, ProductCategoryViewSet, StockRecordViewSet, TransactionViewSet
)
from django.urls import path
from .views import UserUnionList
router = DefaultRouter()

router.register(r"orders", OrdersViewSet, basename='orders')
router.register(r"order-items", Order_itemsViewSet, basename='order-items')
router.register(r"products", ProductViewSet, basename='products')
router.register(r"product_catagory",ProductCategoryViewSet, basename='product_catagory')
router.register(r"stock_record",StockRecordViewSet, basename='stock_record')
router.register(r"transaction",TransactionViewSet, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),
    path('users/', UserUnionList.as_view(), name='users'),
    path('users/<int:pk>/', UserUnionList.as_view(), name='user-detail'),
]