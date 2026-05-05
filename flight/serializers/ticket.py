from rest_framework import serializers
from ..models import Ticket
from .validators import validate_seat_number_format, validate_future_datetime


class TicketListSerializer(serializers.ModelSerializer):
    """
    Returns essential ticket information for browsing.
    Includes flight identification and seat/status info.
    """
    flight_number = serializers.CharField(
        source='flight.flight_number',
        read_only=True
    )
    airline_name = serializers.CharField(
        source='flight.airline.name',
        read_only=True
    )
    passenger_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Ticket
        fields = [
            'id', 'booking_reference', 'passenger_name', 'flight_number',
            'airline_name', 'seat_number', 'ticket_class', 'price', 'status'
        ]
    
    def get_passenger_name(self, obj):
        """Return passenger full name."""
        return f"{obj.passenger.first_name} {obj.passenger.last_name}"


class TicketDetailSerializer(serializers.ModelSerializer):
    """
    Complete Ticket serializer for detail views.
    
    Returns all ticket information including passenger details,
    flight information, and baggage allowance.
    """
    flight_details = serializers.SerializerMethodField()
    passenger_details = serializers.SerializerMethodField()
    
    class Meta:
        model = Ticket
        fields = [
            'id', 'booking_reference', 'passenger', 'passenger_details',
            'flight', 'flight_details', 'seat_number', 'ticket_class',
            'price', 'baggage_weight', 'status'
        ]
    
    def get_flight_details(self, obj):
        """Return key flight information."""
        return {
            'flight_number': obj.flight.flight_number,
            'departure': obj.flight.departure_airport.iata_code,
            'destination': obj.flight.destination_airport.iata_code,
            'departure_time': obj.flight.start_datetime,
            'airline': obj.flight.airline.name if obj.flight.airline else None,
        }
    
    def get_passenger_details(self, obj):
        """Return passenger information."""
        return {
            'name': f"{obj.passenger.first_name} {obj.passenger.last_name}",
            'email': obj.passenger.email,
            'passport': obj.passenger.passport_code,
        }


class TicketCreateSerializer(serializers.ModelSerializer):
    """
    Ticket serializer for booking (create operation).
    
    Validates:
    - Seat number format (e.g., 12A)
    - Flight must be in the future
    - Baggage weight within limits (0-100 kg)
    - Passenger is authenticated and booking for themselves
    
    The 'passenger' field can be overridden by admins but is
    auto-set to current user for regular users.
    """
    seat_number = serializers.CharField(
        max_length=10,
        validators=[validate_seat_number_format]
    )
    baggage_weight = serializers.IntegerField(
        min_value=0,
        max_value=100,
        default=0
    )
    
    class Meta:
        model = Ticket
        fields = ['passenger', 'flight', 'seat_number', 'ticket_class', 'baggage_weight']
    
    def validate(self, data):
        """
        Cross-field validation for Ticket creation.
        
        - Flight must be in future
        - Seat must not already be booked on this flight
        """
        flight = data['flight']
        
        # Validate flight is in future
        validate_future_datetime(flight.start_datetime)
        
        # Check if seat is already booked on this flight
        seat_taken = Ticket.objects.filter(
            flight=flight,
            seat_number=data['seat_number']
        ).exists()
        
        if seat_taken:
            raise serializers.ValidationError(
                f"Seat {data['seat_number']} is already booked on flight {flight.flight_number}"
            )
        
        return data


class TicketUpdateSerializer(serializers.ModelSerializer):
    """
    Ticket serializer for update operations (PATCH).
    
    Only allows updates to:
    - seat_number (if not yet checked in)
    - ticket_class (if not yet checked in)
    - baggage_weight (up to limits)
    
    Cannot change: passenger, flight, status
    """
    seat_number = serializers.CharField(
        max_length=10,
        validators=[validate_seat_number_format],
        required=False
    )
    
    class Meta:
        model = Ticket
        fields = ['seat_number', 'ticket_class', 'baggage_weight']
    
    def validate_seat_number(self, value):
        """Check if new seat is available."""
        if value:
            ticket = self.instance
            seat_taken = Ticket.objects.filter(
                flight=ticket.flight,
                seat_number=value
            ).exclude(id=ticket.id).exists()
            
            if seat_taken:
                raise serializers.ValidationError(
                    f"Seat {value} is already booked on this flight"
                )
        return value
