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
        return f"{obj.passenger_first_name} {obj.passenger_last_name}"


class TicketDetailSerializer(serializers.ModelSerializer):
    """
    Complete Ticket serializer for detail views.
    
    Returns all ticket information including passenger details,
    flight information, and baggage allowance.
    """
    flight_details = serializers.SerializerMethodField()
    passenger_details = serializers.SerializerMethodField()
    order_id = serializers.IntegerField(source='order.id', read_only=True)
    buyer_email = serializers.EmailField(source='order.customer.email', read_only=True)
        
    class Meta:
        model = Ticket
        fields = [
            'id', 'booking_reference', 'order_id', 'buyer_email', 
            'passenger_details','flight', 'flight_details', 'seat_number', 
            'ticket_class', 'price', 'baggage_weight', 'status'
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
            'name': f"{obj.passenger_first_name} {obj.passenger_last_name}",
            'passport': obj.passenger_passport_code,
        }

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
