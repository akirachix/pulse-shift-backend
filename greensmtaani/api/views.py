from django.shortcuts import render
from rest_framework import viewsets
from users.models import Customer, MamaMboga, Address
from orders.models import Orders, Order_items
from products.models import Product, ProductCategory, StockRecord
from .serializer import CustomerSerializer, MamaMbogaSerializer, AddressSerializer, Order_itemsSerializer, OrdersSerializer, ProductSerializer, ProductCategorySerializer, StockRecordSerializer

# Create your views here.
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class MamaMbogaViewSet(viewsets.ModelViewSet):
    queryset = MamaMboga.objects.all()
    serializer_class = MamaMbogaSerializer

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

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


    