from django.shortcuts import render
from rest_framework import viewsets
from payments.models import Transaction

from .serializer import TransactionSerializer




class TransactionViewSet(viewsets.ModelViewSet):
    queryset =Transaction.objects.all()
    serializer_class =TransactionSerializer




