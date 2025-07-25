from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (DietaryPreferenceViewSet, MealPlanViewSet,RecipeViewSet,FetchHistoryViewSet,IngredientViewSet,OrdersViewSet, PaymentViewSet, PayoutViewSet, STKPushView, daraja_callback, Order_itemsViewSet, ProductViewSet, ProductCategoryViewSet, StockRecordViewSet,UserUnionList, reset_request, reset_password )

router = DefaultRouter()
router.register(r"payments", PaymentViewSet, basename='payment')
router.register(r"payouts", PayoutViewSet, basename='payout')
router.register(r"dietary-preferences", DietaryPreferenceViewSet, basename='dietary-preferences')
router.register(r"meal-plans", MealPlanViewSet, basename='meal-plans')
router.register(r"orders", OrdersViewSet, basename='orders')
router.register(r"order-items", Order_itemsViewSet, basename='order-items')
router.register(r"products", ProductViewSet, basename='products')
router.register(r"product-category", ProductCategoryViewSet, basename='productcategory')
router.register(r"stock_record",StockRecordViewSet, basename='stock_record')
router.register(r"recipe", RecipeViewSet, basename='recipe')
router.register(r"ingredient",IngredientViewSet, basename='ingredient')
router.register(r"fetchhistory",FetchHistoryViewSet, basename='fetchhistory')


urlpatterns = [
   path('', include(router.urls)),
   path('daraja/stk-push/', STKPushView.as_view(), name='daraja-stk-push'),
   path('daraja/callback/', daraja_callback, name='daraja-callback'),
   path('users/', UserUnionList.as_view(), name='users'),
   path('users/<int:pk>/', UserUnionList.as_view(), name='user-detail'), 
   path('reset-request/', reset_request, name='reset-request'),
   path('reset-password/', reset_password, name='reset-password'),
]





