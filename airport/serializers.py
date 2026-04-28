from rest_framework import serializers
from .models import Airline, Airport, Airplane

class AirlineSerializer(serializers.ModelSerializer):
    """Serializer for Airline model.
    
    Converts Airline model instances to and from JSON.
    Includes all fields: id, name, iata_code.
    """
    class Meta:
        model = Airline
        fields = '__all__'

class AirportSerializer(serializers.ModelSerializer):
    """Serializer for Airport model.
    
    Converts Airport model instances to and from JSON.
    Includes all fields including foreign keys and many-to-many relationships.
    """
    class Meta:
        model = Airport
        fields = '__all__'

class AirplaneSerializer(serializers.ModelSerializer):
    """Serializer for Airplane model.
    
    Converts Airplane model instances to and from JSON.
    Includes all aircraft details and airline reference.
    """
    class Meta:
        model = Airplane
        fields = '__all__'