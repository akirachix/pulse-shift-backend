from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
ProductViewSet, ProductCategoryViewSet, StockRecordViewSet,
    DietaryPreferenceViewSet, MealPlanViewSet,
    OrdersViewSet, Order_itemsViewSet,TransactionViewSet )
   

router = DefaultRouter()
router.register(r"dietary-preferences", DietaryPreferenceViewSet, basename='dietary-preferences')
router.register(r"meal-plans", MealPlanViewSet, basename='meal-plans')
router.register(r"orders", OrdersViewSet, basename='orders')
router.register(r"order-items", Order_itemsViewSet, basename='order-items')
router.register(r"products", ProductViewSet, basename='products')
router.register(r"product_catagory",ProductCategoryViewSet, basename='product_catagory')
router.register(r"stock_record",StockRecordViewSet, basename='stock_record')
router.register(r"transaction",TransactionViewSet, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),
]