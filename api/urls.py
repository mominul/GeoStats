from django.urls import path
from .views import SearchView, LocationSearchView, AirQualityRankingView

urlpatterns = [
    path('search/<str:query>/', SearchView.as_view(), name='search_api'),
    path('measurement/<str:query>/',LocationSearchView.as_view(), name='measurement_api'),
    path('ranking/', AirQualityRankingView.as_view(), name='ranking-api'),
]