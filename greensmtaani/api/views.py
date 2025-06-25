from django.shortcuts import render
from rest_framework import viewsets
from users.models import Customer, MamaMboga, Address
from orders.models import Orders, Order_items
from nutrition.models import DietaryPreference,MealPlan
from .serializer import CustomerSerializer, MamaMbogaSerializer, AddressSerializer, Order_itemsSerializer, OrdersSerializer,DietaryPreferenceSerializer,MealPlanSerializer

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

class DietaryPreferenceViewSet(viewsets.ModelViewSet):
    queryset = DietaryPreference.objects.all()
    serializer_class = DietaryPreferenceSerializer

class MealPlanViewSet(viewsets.ModelViewSet):
    queryset = MealPlan.objects.all()
    serializer_class = MealPlanSerializer



    