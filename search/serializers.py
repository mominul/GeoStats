from rest_framework import serializers
from .models import Location

class CitySearchSerializer(serializers.ModelSerializer):
     class Meta:
        model = Location
        fields = ['location_id', 'country', 'city', 'name']
    