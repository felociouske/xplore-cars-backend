"""
car_tax/views.py

WHAT THIS FILE DOES:
Defines the two API endpoints the frontend will call:
  1. GET  /api/car-tax/vehicles/   -> search for a vehicle in the CRSP data
  2. POST /api/car-tax/calculate/  -> run the tax calculation

Both are plain function-based views using DRF's @api_view decorator —
no models, no database queries, just calling the functions we already
wrote and tested in data.py and calculator.py.
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from . import data as car_tax_data
from . import calculator
from .serializers import VehicleSearchSerializer, CalculateRequestSerializer


@api_view(["GET"])
def search_vehicles(request):
    """
    GET /api/car-tax/vehicles/?make=MAZDA&model=CX-5&fuel=PETROL&engine_cc=2000

    Returns a list of matching vehicles from the CRSP dataset. The
    frontend calls this as the user types into the search box, and shows
    the results as a picklist — the user picks ONE, and that vehicle's
    data (crsp_value, fuel, engine_cc) gets sent to /calculate/ next.
    """
    # request.query_params holds everything after the "?" in the URL.
    # We validate it through the serializer before using it.
    search_params = VehicleSearchSerializer(data=request.query_params)
    search_params.is_valid(raise_exception=True)
    validated = search_params.validated_data

    results = car_tax_data.search_vehicles(
        make=validated["make"],
        model_keyword=validated["model"],
        fuel=validated["fuel"],
        engine_cc=validated["engine_cc"],
    )

    # Cap results to something reasonable — the frontend shouldn't need
    # to render hundreds of rows in a dropdown.
    return Response(results[:30])


@api_view(["POST"])
def calculate(request):
    """
    POST /api/car-tax/calculate/
    body: { crsp_value, fuel, engine_cc, year_of_manufacture }

    Pure calculation — no vehicle search happens here anymore. The
    frontend is responsible for resolving "which exact vehicle" via
    /vehicles/ first (possibly showing the user a picklist), and only
    calls this endpoint once it has one specific vehicle's real values.
    """
    req = CalculateRequestSerializer(data=request.data)
    if not req.is_valid():
        return Response(
            {"detail": "Please input all the required details needed to estimate your total tax cost."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    validated = req.validated_data

    try:
        result = calculator.calculate_import_tax(
            crsp_value=validated["crsp_value"],
            fuel_type=validated["fuel"],
            engine_cc=validated.get("engine_cc"),
            year_of_manufacture=validated["year_of_manufacture"],
        )
    except calculator.CalculationError as exc:
        return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(result)