from django.shortcuts import render
from api.models import Location

# Create your views here.
def search_view(request):
    return render(request,'search02.html')

def home_view(request):
    return render(request, 'index.html')


def info_view(request, id):
    location = Location.objects.get(location_id=id)
    name = ""
    if location.name:
        name += location.name + ", "
    if location.city:
        name += location.city + ", "

    name += location.country

    data = {
        "id": id,
        "name": name,
        "code": location.code
    }
    return render(request, 'info.html', data)   