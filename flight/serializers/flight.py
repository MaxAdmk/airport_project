"""Flight model serializers."""

from rest_framework import serializers
from ..models import Flight
from .validators import validate_future_datetime, validate_positive_duration


class FlightListSerializer(serializers.ModelSerializer):
    """
    Lightweight Flight serializer for list views.
    
    Returns minimal fields optimized for listing flights.
    Includes flight identification and schedule information.
    """
    departure_airport_name = serializers.CharField(
        source='departure_airport.name',
        read_only=True
    )
    destination_airport_name = serializers.CharField(
        source='destination_airport.name',
        read_only=True
    )
    
    class Meta:
        model = Flight
        fields = [
            'id', 'flight_number', 'departure_airport', 'departure_airport_name',
            'destination_airport', 'destination_airport_name', 'start_datetime',
            'status', 'airline'
        ]


class FlightDetailSerializer(serializers.ModelSerializer):
    """
    Complete Flight serializer for detail views.
    
    Returns all flight information including aircraft, terminal, and gate details.
    Includes full nested representations of related objects.
    """
    
    class Meta:
        model = Flight
        fields = '__all__'


class FlightCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Flight serializer for create and update operations.
    
    Validates:
    - Flight time must be in the future
    - Duration must be positive
    - Departure and destination airports must be different
    - Airplane passenger capacity must accommodate estimated passengers
    
    Used for: POST, PUT, PATCH operations (admin only)
    """
    start_datetime = serializers.DateTimeField(
        validators=[validate_future_datetime]
    )
    approximate_duration = serializers.DurationField(
        validators=[validate_positive_duration]
    )
    
    class Meta:
        model = Flight
        fields = [
            'flight_number', 'departure_airport', 'destination_airport',
            'start_datetime', 'approximate_duration', 'airplane', 'airline'
        ]
    
    def validate(self, data):
        """
        Cross-field validation for Flight.
        
        - Departure and destination must be different
        """
        if data['departure_airport'] == data['destination_airport']:
            raise serializers.ValidationError(
                "Departure and destination airports must be different"
            )
        return data
