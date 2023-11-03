from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CitySearchSerializer, LocationIdSearchSerializer
from .models import Location
import requests
from rest_framework import status

class CitysearchView(APIView):
    def get(self, request, query):
        
        matches = Location.objects.filter(city__icontains=query)[:5]
        serializer = CitySearchSerializer(matches, many=True)
        print(serializer.data)
        return Response(serializer.data)



class LocationSearchView(APIView):
    def get(self, request, query):
        
        location_id = query
        if not location_id:
            return Response({'error': 'Location ID (query parameter) is required.'}, status=status.HTTP_BAD_REQUEST)

        api_url = f'https://api.openaq.org/v2/latest/{location_id}'
        headers = {"accept": "application/json",
                   "X-API-Key": "47ef3bf63537c3d0687ce523ad910cdb30eda1f78fe0d81429fccb8a2af10ec6"}
        response = requests.get(api_url, headers=headers)

        if response.status_code != 200:
            return Response({'error': 'Failed to fetch data from the external API.'}, status=status.HTTP_INTERNAL_SERVER_ERROR)

        data = response.json()
        measurements = data.get('results', [])[0].get('measurements', [])

        relevant_measurements = {
            'temperature': None,
            'pm25': None,
            'pm10': None,
            'pressure': None,
            'humidity': None,
        }

        for measurement in measurements:
            parameter = measurement['parameter']
            if parameter in relevant_measurements:
                relevant_measurements[parameter] = measurement['value']

        serializer = LocationIdSearchSerializer(relevant_measurements)
        return Response(serializer.data)
