from django.shortcuts import render
from rest_framework import viewsets
from users.models import Customer, MamaMboga, Address
from .serializer import CustomerSerialier, MamaMbogaSerialier, AddressSerialier

# Create your views here.
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerialier

class MamaMbogaViewSet(viewsets.ModelViewSet):
    queryset = MamaMboga.objects.all()
    serializer_class = MamaMbogaSerialier

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerialier

    