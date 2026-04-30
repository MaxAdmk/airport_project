"""Airline model serializers."""

from rest_framework import serializers
from ..models import Airline
from .validators import validate_iata_airline_code


class AirlineListSerializer(serializers.ModelSerializer):
    """
    Lightweight Airline serializer for list views.
    
    Returns essential airline information for browsing.
    """
    
    class Meta:
        model = Airline
        fields = ['id', 'name', 'iata_code']


class AirlineDetailSerializer(serializers.ModelSerializer):
    """
    Complete Airline serializer for detail views.
    
    Returns all airline information.
    """
    
    class Meta:
        model = Airline
        fields = '__all__'


class AirlineCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Airline serializer for create and update operations.
    
    Validates:
    - IATA code must be exactly 2 uppercase letters
    - Name must be unique
    - IATA code must be unique
    
    Used for: POST, PUT, PATCH operations (admin only)
    """
    iata_code = serializers.CharField(
        max_length=2,
        validators=[validate_iata_airline_code]
    )
    
    class Meta:
        model = Airline
        fields = ['name', 'iata_code']
