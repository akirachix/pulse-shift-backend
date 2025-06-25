from django.shortcuts import render
from rest_framework import viewsets
<<<<<<< HEAD
from orders.models import Orders, Order_items
from .serializer import  Order_itemsSerializer, OrdersSerializer

# Create your views here.
class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer

class Order_itemsViewSet(viewsets.ModelViewSet):
    queryset = Order_items.objects.all()
    serializer_class =Order_itemsSerializer

=======
from products.models import Product, ProductCategory, StockRecord
from .serializer import  ProductSerializer, ProductCategorySerializer, StockRecordSerializer

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


    
>>>>>>> 7de3fd4e6bbf5778e9b61f799e8886f60f5d2eb9
