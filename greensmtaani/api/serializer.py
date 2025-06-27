from rest_framework import serializers
from users.models import MamaMboga, Customer, Address

from rest_framework import serializers

from orders.models import Orders, Order_items
from payments.models import Transaction
from products.models import Product, ProductCategory, StockRecord 

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class MamaMbogaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MamaMboga
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class UserUnionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField(allow_null=True)
    phone_number = serializers.CharField()
    password = serializers.CharField()
    registration_date = serializers.DateTimeField()
    is_active = serializers.BooleanField()
    user_type = serializers.CharField()

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'
        
class Order_itemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_items

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'
        
class Order_itemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_items


# users APIs       
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
# users APIs
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
