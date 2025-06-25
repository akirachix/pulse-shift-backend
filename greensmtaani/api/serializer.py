from rest_framework import serializers
# from users.models import Customer, MamaMboga, Address
# from orders.models import Orders, Order_items
# from nutrition.models import DietaryPreference,MealPlan
# from products.models import Product, ProductCategory, StockRecord 
from payments.models import Transaction

# users APIs
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'





