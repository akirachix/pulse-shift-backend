from rest_framework import serializers
from users.models import MamaMboga, Customer, Address

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