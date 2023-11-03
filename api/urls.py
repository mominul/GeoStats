from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import SearchView, LocationSearchView

urlpatterns = [
    path('search/', SearchView.as_view(), name='search_api'),
    path('measurement/',LocationSearchView.as_view(), name='measurement_api'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
