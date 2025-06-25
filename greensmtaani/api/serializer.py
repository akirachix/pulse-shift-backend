from rest_framework import serializers

from payments.models import Transaction

# users APIs
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'








