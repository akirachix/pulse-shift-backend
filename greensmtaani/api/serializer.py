from rest_framework import serializers
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




