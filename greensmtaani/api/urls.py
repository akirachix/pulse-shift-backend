from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
ProductViewSet, ProductCategoryViewSet, StockRecordViewSet,
    DietaryPreferenceViewSet, MealPlanViewSet )
   

router = DefaultRouter()
router.register(r"dietary-preferences", DietaryPreferenceViewSet, basename='dietary-preferences')
router.register(r"meal-plans", MealPlanViewSet, basename='meal-plans')



router = DefaultRouter()
router.register(r"products", ProductViewSet, basename='products')
router.register(r"product_catagory",ProductCategoryViewSet, basename='product_catagory')
router.register(r"stock_record",StockRecordViewSet, basename='stock_record')

urlpatterns = [
    path('', include(router.urls)),
]