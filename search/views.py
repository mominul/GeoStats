from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CitySearchSerializer
from .models import Location

class CitysearchView(APIView):
    def get(self, request, query):
        
        matches = Location.objects.filter(city__icontains=query)[:5]
        serializer = CitySearchSerializer(matches, many=True)
        print(serializer.data)
        return Response(serializer.data)
        # return render(request,'search.html')



