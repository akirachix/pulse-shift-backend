from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PaymentViewSet, PayoutViewSet,STKPushView, daraja_callback

)
router = DefaultRouter()

router.register(r"payments",PaymentViewSet, basename='payment')
router.register(r"payouts",PayoutViewSet, basename='payout')

urlpatterns = [
    path('', include(router.urls)),
    path('daraja/stk-push/', STKPushView.as_view(), name='daraja-stk-push'),
    path('daraja/callback/', daraja_callback, name='daraja-callback')
]