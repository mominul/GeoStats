from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CitySearchSerializer, LocationIdSearchSerializer, AirQualityRankingSerializer, CountryStatsSerializer
from .models import Location
import requests
from rest_framework import status
from .iqair import top_ranking_air
import requests
import aqi

def to_list(query):
    list = []
    for item in query:
        list.append(item.__dict__)

    return list

class SearchView(APIView):
    def get(self, request):
        query = request.query_params.get("query")
        list = []
        matches = Location.objects.filter(city__icontains=query)[:5]
        list += to_list(matches)
        matches = Location.objects.filter(name__icontains=query)[:5]
        list += to_list(matches)
        matches = Location.objects.filter(country__icontains=query)[:5]
        list += to_list(matches)
        serializer = CitySearchSerializer(list, many=True)
        return Response(serializer.data)


class LocationSearchView(APIView):
    def get(self, request):
        location_id = request.query_params.get("id")
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
        
        aqi_value = aqi.to_aqi([
            (aqi.POLLUTANT_PM25, relevant_measurements["pm25"]),
            (aqi.POLLUTANT_PM10, relevant_measurements["pm10"]),
            # (aqi.POLLUTANT_O3_8H, '0.087')
        ])

        relevant_measurements['aqi'] = aqi_value

        serializer = LocationIdSearchSerializer(relevant_measurements)
        return Response(serializer.data)

class AirQualityRankingView(APIView):
    def get(self, request):
        max = int(request.query_params.get("top"))

        data = top_ranking_air(max)

        polluted_serializer = AirQualityRankingSerializer(data["polluted"], many=True)
        cleanest_serializer = AirQualityRankingSerializer(data["cleanest"], many=True)

        response_data = {
            "polluted": polluted_serializer.data,
            "cleanest": cleanest_serializer.data
        }

        return Response(response_data)

class CountryStatsView(APIView):
    def get(self, request):
        code = request.query_params.get('code')
        response = requests.get(f'https://api.worldbank.org/v2/countries/{code}/indicators/NY.GDP.MKTP.CD?per_page=1&format=json').json()
        gdp = response[1][0]["value"]

        response = requests.get(f'https://api.worldbank.org/v2/countries/{code}/indicators/NY.GDP.PCAP.CD?per_page=1&format=json').json()
        gdp_per_capita = response[1][0]["value"]

        response = requests.get(f'https://api.worldbank.org/v2/countries/{code}/indicators/NY.GDP.MKTP.KD.ZG?per_page=1&format=json').json()
        gdp_growth = response[1][0]["value"]

        response = requests.get(f'https://api.worldbank.org/v2/countries/{code}/indicators/SP.POP.TOTL?per_page=1&format=json').json()
        population = response[1][0]["value"]

        response = requests.get(f'https://api.worldbank.org/v2/countries/{code}/indicators/SP.POP.GROW?per_page=1&format=json').json()
        population_growth = response[1][0]["value"]

        # serializer = CountryStatsSerializer(gdp, gdp_per_capita, gdp_growth, population, population_growth, many=True)
        data = {
            "gdp": gdp,
            "gdp_per_capita": gdp_per_capita,
            "gdp_growth": gdp_growth,
            "population": population,
            "population_growth": population_growth
        }
        return Response(data)