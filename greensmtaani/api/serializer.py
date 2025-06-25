from rest_framework import serializers
# from users.models import Customer, MamaMboga, Address
# from orders.models import Orders, Order_items
# from nutrition.models import DietaryPreference,MealPlan
# from products.models import Product, ProductCategory, StockRecord 
from payments.models import Transaction
from products.models import Product, ProductCategory, StockRecord 

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






