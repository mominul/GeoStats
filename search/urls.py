from django.urls import path
from .views import CitysearchView, LocationSearchView

urlpatterns = [
    path('city/<str:query>/', CitysearchView.as_view(), name='city-search'),
    path('search/', LocationSearchView.as_view(), name='location-search'),
    path('locationId/<str:query>/',LocationSearchView.as_view(), name='location-search'),
]