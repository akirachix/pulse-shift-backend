from django.shortcuts import render
from rest_framework import viewsets
from nutrition.models import DietaryPreference,MealPlan
from .serializer import  DietaryPreferenceSerializer,MealPlanSerializer

# Create your views here.
class DietaryPreferenceViewSet(viewsets.ModelViewSet):
    queryset = DietaryPreference.objects.all()
    serializer_class = DietaryPreferenceSerializer

class MealPlanViewSet(viewsets.ModelViewSet):
    queryset = MealPlan.objects.all()
    serializer_class = MealPlanSerializer
