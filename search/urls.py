from django.urls import path
from .views import CitysearchView

urlpatterns = [
    path('<str:query>/', CitysearchView.as_view(), name='city-search'),
]