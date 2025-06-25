from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductViewSet, ProductCategoryViewSet, StockRecordViewSet
   TransactionViewSet

)
router = DefaultRouter()
router.register(r"products", ProductViewSet, basename='products')
router.register(r"product_catagory",ProductCategoryViewSet, basename='product_catagory')
router.register(r"stock_record",StockRecordViewSet, basename='stock_record')

router.register(r"transaction",TransactionViewSet, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),
]