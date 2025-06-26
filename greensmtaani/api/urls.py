from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DietaryPreferenceViewSet, MealPlanViewSet )
   

router = DefaultRouter()
router.register(r"dietary-preferences", DietaryPreferenceViewSet, basename='dietary-preferences')
router.register(r"meal-plans", MealPlanViewSet, basename='meal-plans')
urlpatterns = [
    path('', include(router.urls)),
]