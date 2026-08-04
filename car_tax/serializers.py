"""
car_tax/serializers.py

WHAT THIS FILE DOES:
Defines the expected shape of data for each API request. DRF uses these
to automatically validate incoming requests — if the frontend sends
something malformed (e.g. missing a required field, or a string where a
number should be), DRF rejects it with a clear error BEFORE it ever
reaches our calculation code. This means calculator.py never has to
defend against bad input itself.
"""
from rest_framework import serializers


class VehicleSearchSerializer(serializers.Serializer):
    """
    Validates the query parameters for GET /api/car-tax/vehicles/
    All fields are optional except nothing is strictly required — an
    empty search just returns nothing useful, which is fine.
    """
    make = serializers.CharField(required=False, allow_blank=True, default="")
    model = serializers.CharField(required=False, allow_blank=True, default="")
    fuel = serializers.CharField(required=False, allow_blank=True, default="")
    engine_cc = serializers.IntegerField(required=False, allow_null=True, default=None)


class CalculateRequestSerializer(serializers.Serializer):
    """
    Validates the body for POST /api/car-tax/calculate/

    This endpoint no longer searches anything — it expects the EXACT
    vehicle values already known (typically because the frontend just
    got them from a /vehicles/ search result the user clicked on).
    This removes all ambiguity: there's nothing left to "match", so
    there's no way to get a "multiple matches" situation here anymore.
    """
    crsp_value = serializers.FloatField(min_value=1)
    fuel = serializers.CharField()
    engine_cc = serializers.IntegerField(required=False, allow_null=True)
    year_of_manufacture = serializers.IntegerField(min_value=1990, max_value=2100)