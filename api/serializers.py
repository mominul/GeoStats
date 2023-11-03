from rest_framework import serializers
from .models import Location

class CitySearchSerializer(serializers.ModelSerializer):
     class Meta:
        model = Location
        fields = ['location_id', 'country', 'city', 'name']


class LocationIdSearchSerializer(serializers.Serializer):
   temperature = serializers.DecimalField(max_digits=5, decimal_places=2)
   pm25 = serializers.DecimalField(max_digits=6, decimal_places=2)
   pm10 = serializers.DecimalField(max_digits=6, decimal_places=2)
   pressure = serializers.DecimalField(max_digits=7, decimal_places=2)
   humidity = serializers.DecimalField(max_digits=5, decimal_places=2)

class AirQualityRankingSerializer(serializers.Serializer):
    flag = serializers.CharField()
    city = serializers.CharField()
    score = serializers.CharField()
    