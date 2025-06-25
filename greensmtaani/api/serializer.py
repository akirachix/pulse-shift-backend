from rest_framework import serializers
from nutrition.models import DietaryPreference,MealPlan
# users APIs
class DietaryPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietaryPreference
        fields = '__all__'
class MealPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealPlan
        fields = '__all__'        
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





