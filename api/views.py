import random
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status,generics
from rest_framework.response import Response
from rest_framework import status
from .sandbox import MpesaAPI
from django.db.models import Value as V, CharField, F
from django.shortcuts import render
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from nutrition.models import DietaryPreference,MealPlan, FetchHistory,Recipe,Ingredient
from orders.models import Orders, Order_items
from users.models import Customer, MamaMboga
from products.models import Product, ProductCategory, StockRecord
from payments.models import Payment, Payout
import logging
logger = logging.getLogger(__name__)
from .serializer import RegisterSerializer, LoginSerializer, UserProfileUnionSerializer,PayoutSerializer,PaymentSerializer,CustomerSerializer, MamaMbogaSerializer, DietaryPreferenceSerializer,MealPlanSerializer, Order_itemsSerializer, OrdersSerializer, ProductSerializer, ProductCategorySerializer, StockRecordSerializer,RecipeSerializer,IngredientSerializer,FetchHistorySerializer,STKPushSerializer

from rest_framework import status, generics, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authtoken.models import Token
from django.contrib.auth import login


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        role = None
        if hasattr(request.user, 'admin_mod_profile'):
            role = request.user.admin_mod_profile.role
        
        if role in ['admin', 'moderator']:
            return True
        
        if request.user.is_staff: 
            return True

        return hasattr(obj, 'user') and obj.user == request.user
    

class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'customer')

class IsMamaMboga(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'mama_mboga')

class IsOrderCustomerOrVendor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        role = None
        if hasattr(request.user, 'admin_mod_profile'):
            role = request.user.admin_mod_profile.role
        if role in ['admin', 'moderator']:
            return True
        if request.user.is_staff:
            return True
        if hasattr(request.user, 'customer') and obj.customer.user == request.user:
            return True
        if hasattr(request.user, 'mama_mboga') and obj.vendor.user == request.user:
            return True
        return False

class IsProfileOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        role = None
        if hasattr(request.user, 'admin_mod_profile'):
            role = request.user.admin_mod_profile.role
        
        if role in ['admin', 'moderator']:
            return True

        if request.user.is_staff:
            return True
        return obj.user == request.user

class RegisterView(APIView):
    permission_classes = [AllowAny]  

    def post(self, request):
        data = request.data
        user_type = data.get('user_type')

        if user_type in ['customer', 'mama_mboga', 'admin', 'moderator']:
            serializer = RegisterSerializer(data=data) 
            if serializer.is_valid():
                user = serializer.save() 

        profile = None

        if user_type == 'customer':
            customer_serializer = CustomerSerializer(data=data)
            customer_serializer.is_valid(raise_exception=True)
            profile = customer_serializer.save(user=user)
        elif user_type == 'mama_mboga':
            mama_mboga_serializer = MamaMbogaSerializer(data=data)
            mama_mboga_serializer.is_valid(raise_exception=True)
            profile = mama_mboga_serializer.save(user=user)

        if profile:
            return Response({'detail': f'{user_type.capitalize()} registered successfully', 'user_id': user.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        login(request, user)
        token, created = Token.objects.get_or_create(user=user)

        # Determine user_type
        if hasattr(user, 'customer'):
            user_type = 'customer'
            profile = user.customer
        elif hasattr(user, 'mama_mboga'):
            user_type = 'mama_mboga'
            profile = user.mama_mboga
        elif hasattr(user, 'admin_mod_profile'):
            user_type = user.admin_mod_profile.role
            profile = user.admin_mod_profile
        else:
            user_type = 'user'
            profile = user
            

        user_data = UserProfileUnionSerializer(profile).data
        user_data['user_type'] = user_type

        return Response({
            "user": user_data,
            "token": token.key
        })

class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        from django.contrib.auth import logout
        logout(request)
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated, IsProfileOwnerOrAdmin]
    
    def get(self, request):
        user = request.user
        if hasattr(user, 'customer'):
            profile = user.customer
        elif hasattr(user, 'mama_mboga'):
            profile = user.mama_mboga
        elif hasattr(user, 'admin'):
            profile = user.admin
        else:
            return Response(...)
            
        serializer = UserProfileUnionSerializer(profile)
        return Response(serializer.data)





class UserUnionList(APIView):
    permission_classes = [IsAdminUser] 

    def get(self, request, pk=None):

        if pk is None:
            customers = Customer.objects.all()
            mamambogas = MamaMboga.objects.all()
            union = list(customers) + list(mamambogas)
            serializer = UserProfileUnionSerializer(union, many=True)
            return Response(serializer.data)
        
        else:
            try:
                user_instance = Customer.objects.get(pk=pk)
            except Customer.DoesNotExist:
                try:
                    user_instance = MamaMboga.objects.get(pk=pk)
                except MamaMboga.DoesNotExist:
                    return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            serializer = UserProfileUnionSerializer(user_instance)
            return Response(serializer.data)
        
    def post(self, request):
        # Registration should go through RegisterView
        return Response({'error': 'Use /api/register/ for user registration'}, 
                       status=status.HTTP_405_METHOD_NOT_ALLOWED)


    

    def patch(self, request, pk):
        permission_classes = [IsAuthenticated, IsProfileOwnerOrAdmin]

        user_type = request.data.get('user_type')
        instance = None
        if user_type == 'customer':
            instance = Customer.objects.filter(pk=pk).first()
            serializer_class = CustomerSerializer
        elif user_type == 'mama_mboga':
            instance = MamaMboga.objects.filter(pk=pk).first()
            serializer_class = MamaMbogaSerializer
        else:
            return Response({'error': 'Invalid user_type'}, status=status.HTTP_400_BAD_REQUEST)
        if not instance:
            return Response({'error': 'User not found!'}, status=status.HTTP_404_NOT_FOUND)
        serializer = serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        permission_classes = [IsAuthenticated, IsAdminUser]

        user_type = request.data.get('user_type')
        if user_type == 'customer':
            instance = Customer.objects.filter(pk=pk).first()
        elif user_type == 'mama_mboga':
            instance = MamaMboga.objects.filter(pk=pk).first()
        else:
            return Response({'error': 'Invalid user_type'}, status=status.HTTP_400_BAD_REQUEST)
        if not instance:
            return Response({'error': 'User not found!'}, status=status.HTTP_404_NOT_FOUND)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class DietaryPreferenceViewSet(viewsets.ModelViewSet):
    queryset = DietaryPreference.objects.all()
    serializer_class = DietaryPreferenceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer
    permission_classes = [IsAuthenticated, IsOrderCustomerOrVendor]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Orders.objects.all()
        if hasattr(user, 'customer'):
            return Orders.objects.filter(customer=user.customer)
        if hasattr(user, 'mama_mboga'):
            return Orders.objects.filter(vendor=user.mama_mboga)
        return Orders.objects.none()


class Order_itemsViewSet(viewsets.ModelViewSet):
    queryset = Order_items.objects.all()
    serializer_class =Order_itemsSerializer
    permission_classes = [IsAuthenticated, IsOrderCustomerOrVendor] 

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class =ProductSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        elif self.action in ['create']:
            return [permissions.IsAuthenticated(), IsMamaMboga()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsMamaMboga()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user.mama_mboga)


class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class =ProductCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class StockRecordViewSet(viewsets.ModelViewSet):
    queryset = StockRecord.objects.all()
    serializer_class =StockRecordSerializer
    permission_classes = [IsAuthenticated, IsMamaMboga]


class PaymentViewSet(viewsets.ModelViewSet):
      queryset = Payment.objects.all()
      serializer_class =PaymentSerializer
      permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

class PayoutViewSet(viewsets.ModelViewSet):
      queryset = Payout.objects.all()
      serializer_class =PayoutSerializer
      permission_classes = [IsAuthenticated, IsAdminUser] 


class STKPushView(APIView):
    permission_classes = [IsAuthenticated] 

    def post(self, request):
        serializer = STKPushSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            daraja = MpesaAPI()
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
    permission_classes = [AllowAny]
    print("Daraja Callback Data:", request.data)
    return Response({"ResultCode": 0, "ResultDesc": "Accepted"})


class MealPlanViewSet(viewsets.ModelViewSet):
    queryset = MealPlan.objects.all()
    serializer_class = MealPlanSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class IngredientViewSet(viewsets.ModelViewSet):
       queryset = Ingredient.objects.all()
       serializer_class = IngredientSerializer
       permission_classes = [IsAuthenticatedOrReadOnly]

class RecipeViewSet(viewsets.ModelViewSet):
       queryset = Recipe.objects.all()
       serializer_class = RecipeSerializer
       permission_classes = [IsAuthenticatedOrReadOnly]
class FetchHistoryViewSet(viewsets.ModelViewSet):
       queryset = FetchHistory.objects.all()
       serializer_class = FetchHistorySerializer
       permission_classes = [IsAdminUser]




