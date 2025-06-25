from rest_framework import serializers
from users.models import Customer, MamaMboga, Address
from orders.models import Orders, Order_items
from payments.models import Transaction

# users APIs
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

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'
        
class Order_itemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_items
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Transaction
        fields='__all__'


