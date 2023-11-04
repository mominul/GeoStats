from django.shortcuts import render

# Create your views here.
def search_view(request):
    return render(request,'search02.html')

def home_view(request):
    return render(request, 'index.html')


def info_view(request, id):
    return render(request, 'info.html', {"id": id})   