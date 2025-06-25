from django.shortcuts import render
from rest_framework import viewsets
from nutrition.models import DietaryPreference,MealPlan

from orders.models import Orders, Order_items
from payment.models import Transaction
from .serializer import  Order_itemsSerializer, OrdersSerializer, ProductSerializer, ProductCategorySerializer, StockRecordSerializer, TransactionSerializer,DietaryPreferenceSerializer,MealPlanSerializer
from products.models import Product, ProductCategory, StockRecord



# Create your views here.
class DietaryPreferenceViewSet(viewsets.ModelViewSet):
    queryset = DietaryPreference.objects.all()
    serializer_class = DietaryPreferenceSerializer

class MealPlanViewSet(viewsets.ModelViewSet):
    queryset = MealPlan.objects.all()
    serializer_class = MealPlanSerializer

# Create your views here.
class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer

class Order_itemsViewSet(viewsets.ModelViewSet):
    queryset = Order_items.objects.all()
    serializer_class =Order_itemsSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class =ProductSerializer

class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class =ProductCategorySerializer

class StockRecordViewSet(viewsets.ModelViewSet):
    queryset = StockRecord.objects.all()
    serializer_class =StockRecordSerializer
class TransactionViewSet(viewsets.ModelViewSet):
      queryset = Transaction.objects.all()
    serializer_class =TransactionSerializer



