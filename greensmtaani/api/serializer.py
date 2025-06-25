from rest_framework import serializers
from orders.models import Orders, Order_items



class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'
        
class Order_itemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_items
        fields = '__all__'




