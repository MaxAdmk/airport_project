"""Airplane model serializers."""

from rest_framework import serializers
from ..models import Airplane
from .validators import validate_positive_integer


class AirplaneListSerializer(serializers.ModelSerializer):
    """
    Lightweight Airplane serializer for list views.
    
    Returns essential aircraft information for browsing.
    """
    airline_name = serializers.CharField(
        source='airline.name',
        read_only=True
    )
    
    class Meta:
        model = Airplane
        fields = ['id', 'model_name', 'tail_number', 'airline_name', 'num_of_passengers']


class AirplaneDetailSerializer(serializers.ModelSerializer):
    """
    Complete Airplane serializer for detail views.
    
    Returns all aircraft information including crew and airline details.
    """
    
    class Meta:
        model = Airplane
        fields = '__all__'


class AirplaneCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Airplane serializer for create and update operations.
    
    Validates:
    - Number of passengers must be positive (> 0)
    - Crew amount must be positive (> 0)
    - Tail number must be unique
    
    Used for: POST, PUT, PATCH operations (admin only)
    """
    num_of_passengers = serializers.IntegerField(
        validators=[validate_positive_integer]
    )
    crew_amount = serializers.IntegerField(
        validators=[validate_positive_integer]
    )
    
    class Meta:
        model = Airplane
        fields = ['model_name', 'tail_number', 'num_of_passengers', 'crew_amount', 'airline']
