from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from users.models import Customer, MamaMboga
from django.db.models import Value as V, CharField, F
from django.shortcuts import render
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from orders.models import Orders, Order_items
from payments.models import Payment, Payout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .sandbox import MpesaAPI
from .serializer import STKPushSerializer
from nutrition.models import DietaryPreference,MealPlan
from .serializer import  UserUnionSerializer, CustomerSerializer, MamaMbogaSerializer, DietaryPreferenceSerializer,MealPlanSerializer, Order_itemsSerializer, OrdersSerializer, ProductSerializer, ProductCategorySerializer, StockRecordSerializer
from orders.models import Orders, Order_items
from products.models import Product, ProductCategory, StockRecord

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import  Order_itemsSerializer, OrdersSerializer, ProductSerializer, ProductCategorySerializer, StockRecordSerializer, PaymentSerializer, PayoutSerializer
from products.models import Product, ProductCategory, StockRecord

class UserUnionList(APIView):
    def get(self, request):
        customers = Customer.objects.annotate(
            user_type=V('customer', output_field=CharField()),
            id=F('customer_id')
        ).values(
            'id', 'first_name', 'last_name', 'email', 'phone_number', 'password',
            'registration_date', 'is_active', 'user_type'
        )
        mamambogas = MamaMboga.objects.annotate(
            user_type=V('mama_mboga', output_field=CharField()),
            id=F('mama_mboga_id')
        ).values(
            'id', 'first_name', 'last_name', 'email', 'phone_number', 'password',
            'registration_date', 'is_active', 'user_type'
        )
        union = customers.union(mamambogas)
        serializer = UserUnionSerializer(union, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data
        user_type = data.get('user_type')
        if user_type == 'customer':
            serializer = CustomerSerializer(data=data)
        elif user_type == 'mama_mboga':
            serializer = MamaMbogaSerializer(data=data)
        else:
            return Response({'error': 'Unknown user_type'}, status=status.HTTP_400_BAD_REQUEST)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, pk):
        user_type = request.data.get('user_type')
        if user_type == 'customer':
            try:
                user = Customer.objects.get(pk=pk)
            except Customer.DoesNotExist:
                return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = CustomerSerializer(user, data=request.data, partial=True)
        elif user_type == 'mama_mboga':
            try:
                user = MamaMboga.objects.get(pk=pk)
            except MamaMboga.DoesNotExist:
                return Response({'error': 'MamaMboga not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = MamaMbogaSerializer(user, data=request.data, partial=True)
        else:
            return Response({'error': 'Invalid user_type'}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user_type = request.data.get('user_type')
        if user_type == 'customer':
            try:
                user = Customer.objects.get(pk=pk)
            except Customer.DoesNotExist:
                return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
            user.delete()
        elif user_type == 'mama_mboga':
            try:
                user = MamaMboga.objects.get(pk=pk)
            except MamaMboga.DoesNotExist:
                return Response({'error': 'MamaMboga not found'}, status=status.HTTP_404_NOT_FOUND)
            user.delete()
        else:
            return Response({'error': 'Invalid user_type'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class DietaryPreferenceViewSet(viewsets.ModelViewSet):
    queryset = DietaryPreference.objects.all()
    serializer_class = DietaryPreferenceSerializer

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

class PaymentViewSet(viewsets.ModelViewSet):
      queryset = Payment.objects.all()
      serializer_class =PaymentSerializer

class PayoutViewSet(viewsets.ModelViewSet):
      queryset = Payout.objects.all()
      serializer_class =PayoutSerializer


class STKPushView(APIView):
    def post(self, request):
        serializer = STKPushSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            daraja = MpesaAPIAPI()
            response = daraja.stk_push(
                phone_number=data['phone_number'],
                amount=data['amount'],
                account_reference=data['account_reference'],
                transaction_desc=data['transaction_desc']
            )
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
def daraja_callback(request):
    print("Daraja Callback Data:", request.data)
    return Response({"ResultCode": 0, "ResultDesc": "Accepted"})




class MealPlanViewSet(viewsets.ModelViewSet):
    queryset = MealPlan.objects.all()
    serializer_class = MealPlanSerializer