from rest_framework import serializers
from .models import GeoLocation

class GeoLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoLocation
        fields = ['id', 'name', 'latitude', 'longitude', 'is_mama_mboga', 'address']
