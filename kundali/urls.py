# kundali/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.kundali_home, name='kundali_home'),
    path('generate/', views.generate_kundali, name='generate_kundali'),
    path('get-cities/', views.get_cities, name='get_cities'),
    path('search-location/', views.search_location, name='search_location'),
]