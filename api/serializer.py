from dataclasses import fields
from rest_framework import serializers
from users.models import MamaMboga, Customer, Address, AdminModeratorProfile
from nutrition.models import DietaryPreference, MealPlan,Recipe,Ingredient,FetchHistory
from orders.models import Orders, Order_items
from products.models import Product, ProductCategory, StockRecord
from payments.models import Payment, Payout
from locations.models import GeoLocation
from django.contrib.auth.models import User
from django.contrib.auth import authenticate




class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']


class RegisterSerializer(serializers.ModelSerializer):
    user_type = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'user_type')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user_type = validated_data.pop('user_type', None)
        password = validated_data.pop('password')

        # Create user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=password,
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
        if user_type in ['admin', 'moderator']:
            user.is_staff = True
            user.save()

            AdminModeratorProfile.objects.create(user=user, role=user_type)
        else:
            user.is_staff = False
            user.save()

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")
    


class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    user_data = UserSerializer(write_only=True)

    class Meta:
        model = Customer
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user_data')
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        customer = Customer.objects.create(user=user, **validated_data)
        return customer


class MamaMbogaSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    user_data = UserSerializer(write_only=True)  # write-only nested input data

    class Meta:
        model = MamaMboga
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user_data')
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        mama_mboga = MamaMboga.objects.create(user=user, **validated_data)

        if mama_mboga.location_latitude and mama_mboga.location_longitude:
            GeoLocation.objects.create(
                name=mama_mboga.kiosk_name,
                latitude=mama_mboga.location_latitude,
                longitude=mama_mboga.location_longitude,
                is_mama_mboga=True,
                address=mama_mboga.address_description or ""
            )

        return mama_mboga


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class UserProfileUnionSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='user.id')
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.EmailField(source='user.email')
    user_type = serializers.SerializerMethodField()
    phone_number = serializers.CharField()
    image_url = serializers.URLField()
    registration_date = serializers.DateTimeField()
    is_active = serializers.BooleanField(source='user.is_active')
    kiosk_name = serializers.CharField(required=False)  
    
    def get_user_type(self, obj):
        if isinstance(obj, Customer):
            return 'customer'
        if isinstance(obj, MamaMboga):
            return 'mamamboga'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if hasattr(instance, 'customer'):
            customer_data = CustomerSerializer(instance.customer).data
            data.update(customer_data)
            dietary_prefs = getattr(instance.customer, 'dietary_preferences', None)
            if dietary_prefs is not None:
                data['dietary_preferences'] = DietaryPreferenceSerializer(
                    dietary_prefs.all(), many=True
                ).data
        elif hasattr(instance, 'mama_mboga'):
            mama_data = MamaMbogaSerializer(instance.mama_mboga).data
            data.update(mama_data)
        elif hasattr(instance, 'customer'):
            data.update({
                'dietary_preferences': DietaryPreferenceSerializer(
                    instance.customer.dietary_preferences.all(), 
                    many=True
                ).data
            })

        return data
  

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'

class Order_itemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_items   
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'

class StockRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockRecord
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class PayoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payout
        fields = '__all__'

class STKPushSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    account_reference = serializers.CharField(max_length=12, default="AZ12375")
    transaction_desc = serializers.CharField()

class DietaryPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietaryPreference
        fields = '__all__'

class MealPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealPlan
        fields = '__all__'

class DietaryPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietaryPreference
        fields = '__all__'
class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'
class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'

class FetchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FetchHistory
        fields ='__all__'



# {
#   "user_type": "mama_mboga",
#   "user_data": {
#     "username": "sammwangi",
#     "password": "changeme789",
#     "email": "samumwangi@example.com",
#     "first_name": "Samantha",
#     "last_name": "Mwangi"
#   },
#   "phone_number": "0709111222"
# }


