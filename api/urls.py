from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import SearchView, LocationSearchView, AirQualityRankingView, CountryStatsView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version='v1',
        description="Your API description",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="contact@yourapp.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('search/', SearchView.as_view(), name='search_api'),
    path('measurement/',LocationSearchView.as_view(), name='measurement_api'),
    path('ranking/', AirQualityRankingView.as_view(), name='ranking_api'),
    path('stats/', CountryStatsView.as_view(), name='stats_api'),

    path('swagger<str:format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
