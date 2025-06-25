from rest_framework import serializers

from orders.models import Orders, Order_items
from payments.models import Transaction
from products.models import Product, ProductCategory, StockRecord 


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






