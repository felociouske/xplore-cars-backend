"""
car_tax/urls.py

Maps URL paths to the view functions in views.py. This file gets
"included" into your project's main urls.py (shown below).
"""
from django.urls import path
from . import views

urlpatterns = [
    path("vehicles/", views.search_vehicles, name="car-tax-search-vehicles"),
    path("calculate/", views.calculate, name="car-tax-calculate"),
]