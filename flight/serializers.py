from rest_framework import serializers
from .models import Flight, Ticket

class FlightSerializer(serializers.ModelSerializer):
    """Serializer for Flight model.
    
    Converts Flight model instances to and from JSON.
    Includes flight details, airport references, schedule, status, and aircraft info.
    """
    class Meta:
        model = Flight
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    """Serializer for Ticket model.
    
    Converts Ticket model instances to and from JSON.
    Includes booking details, passenger reference, seat assignment, and pricing.
    """
    class Meta:
        model = Ticket
        fields = '__all__'    