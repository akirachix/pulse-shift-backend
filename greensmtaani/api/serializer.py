from rest_framework import serializers
from users.models import Customer, MamaMboga, Address

# users APIs
class CustomerSerialier(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class MamaMbogaSerialier(serializers.ModelSerializer):
    class Meta:
        model = MamaMboga
        fields = '__all__'

class AddressSerialier(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'