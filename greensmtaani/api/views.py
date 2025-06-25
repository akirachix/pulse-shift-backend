from django.shortcuts import render
from rest_framework import viewsets
from products.models import Product, ProductCategory, StockRecord
from .serializer import ProductSerializer, ProductCategorySerializer, StockRecordSerializer

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


    