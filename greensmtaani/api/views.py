from django.shortcuts import render
from rest_framework import viewsets
from orders.models import Orders, Order_items
from .serializer import  Order_itemsSerializer, OrdersSerializer

# Create your views here.
class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer

class Order_itemsViewSet(viewsets.ModelViewSet):
    queryset = Order_items.objects.all()
    serializer_class =Order_itemsSerializer

