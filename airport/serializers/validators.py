import re
from rest_framework import serializers


def validate_iata_airline_code(value):
    """
    Validate IATA airline code format.
    
    Must be exactly 2 uppercase letters (e.g., AA, BA, UA).
    """
    if not re.match(r'^[A-Z]{2}$', value):
        raise serializers.ValidationError(
            "IATA airline code must be exactly 2 uppercase letters (e.g., AA, BA)"
        )


def validate_iata_airport_code(value):
    """
    Validate IATA airport code format.
    
    Must be exactly 3 uppercase letters (e.g., JFK, LAX, LHR).
    """
    if not re.match(r'^[A-Z]{3}$', value):
        raise serializers.ValidationError(
            "IATA airport code must be exactly 3 uppercase letters (e.g., JFK, LAX)"
        )


def validate_positive_integer(value):
    """
    Validate that value is a positive integer.
    """
    if value <= 0:
        raise serializers.ValidationError(
            "Value must be greater than zero"
        )
