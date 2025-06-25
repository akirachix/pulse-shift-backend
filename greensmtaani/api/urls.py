from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
<<<<<<< HEAD
    OrdersViewSet, Order_itemsViewSet

)
router = DefaultRouter()

router.register(r"orders", OrdersViewSet, basename='orders')
router.register(r"order-items", Order_itemsViewSet, basename='order-items')

=======
    ProductViewSet, ProductCategoryViewSet, StockRecordViewSet
   TransactionViewSet

)
router = DefaultRouter()
router.register(r"products", ProductViewSet, basename='products')
router.register(r"product_catagory",ProductCategoryViewSet, basename='product_catagory')
router.register(r"stock_record",StockRecordViewSet, basename='stock_record')
>>>>>>> 7de3fd4e6bbf5778e9b61f799e8886f60f5d2eb9

router.register(r"transaction",TransactionViewSet, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),
]