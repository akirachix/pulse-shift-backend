from django.shortcuts import render
from rest_framework import viewsets
from nutrition.models import DietaryPreference,MealPlan
from .serializer import DietaryPreferenceSerializer,MealPlanSerializer
from products.models import Product, ProductCategory, StockRecord
from .serializer import  ProductSerializer, ProductCategorySerializer, StockRecordSerializer


# Create your views here.
class DietaryPreferenceViewSet(viewsets.ModelViewSet):
    queryset = DietaryPreference.objects.all()
    serializer_class = DietaryPreferenceSerializer

class MealPlanViewSet(viewsets.ModelViewSet):
    queryset = MealPlan.objects.all()
    serializer_class = MealPlanSerializer

# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class =ProductSerializer

class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class =ProductCategorySerializer

class StockRecordViewSet(viewsets.ModelViewSet):
    queryset = StockRecord.objects.all()
    serializer_class =StockRecordSerializer



    