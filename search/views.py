from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CitySearchSerializer
from .models import Location

def to_list(query):
    list = []
    for item in query:
        list.append(item.__dict__)

    return list

class CitysearchView(APIView):
    def get(self, request, query):
        list = []
        matches = Location.objects.filter(city__icontains=query)[:5]
        list += to_list(matches)
        matches = Location.objects.filter(name__icontains=query)[:5]
        list += to_list(matches)
        matches = Location.objects.filter(country__icontains=query)[:5]
        list += to_list(matches)
        serializer = CitySearchSerializer(list, many=True)
        print(serializer.data)
        return Response(serializer.data)
        # return render(request,'search.html')



