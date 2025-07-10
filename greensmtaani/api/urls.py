from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PaymentViewSet, PayoutViewSet, STKPushView, daraja_callback,
    DietaryPreferenceViewSet, MealPlanViewSet,
    OrdersViewSet, Order_itemsViewSet, ProductViewSet,
    ProductCategoryViewSet, StockRecordViewSet, UserUnionList
)

router = DefaultRouter()
router.register(r"payments", PaymentViewSet, basename='payment')
router.register(r"payouts", PayoutViewSet, basename='payout')
router.register(r"dietary-preferences", DietaryPreferenceViewSet, basename='dietary-preferences')
router.register(r"meal-plans", MealPlanViewSet, basename='meal-plans')
router.register(r"orders", OrdersViewSet, basename='orders')
router.register(r"order-items", Order_itemsViewSet, basename='order-items')
router.register(r"products", ProductViewSet, basename='products')
router.register(r"product-categories", ProductCategoryViewSet, basename='productcategory')
router.register(r"stock-records", StockRecordViewSet, basename='stockrecord')

urlpatterns = [
    path('', include(router.urls)),
    path('daraja/stk-push/', STKPushView.as_view(), name='daraja-stk-push'),
    path('daraja/callback/', daraja_callback, name='daraja-callback'),
    path('users/', UserUnionList.as_view(), name='users'),
    path('users/<int:pk>/', UserUnionList.as_view(), name='user-detail'),
]
