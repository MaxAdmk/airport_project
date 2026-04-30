"""Airport model serializers."""

from rest_framework import serializers
from ..models import Airport
from .validators import validate_iata_airport_code


class AirportListSerializer(serializers.ModelSerializer):
    """
    Lightweight Airport serializer for list views.
    
    Returns essential airport information for browsing.
    """
    country_name = serializers.CharField(
        source='country.name',
        read_only=True
    )
    city_name = serializers.CharField(
        source='city.name',
        read_only=True
    )
    
    class Meta:
        model = Airport
        fields = ['id', 'name', 'iata_code', 'city_name', 'country_name']


class AirportDetailSerializer(serializers.ModelSerializer):
    """
    Complete Airport serializer for detail views.
    
    Returns all airport information including related cities and countries.
    """
    
    class Meta:
        model = Airport
        fields = '__all__'


class AirportCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Airport serializer for create and update operations.
    
    Validates:
    - IATA code must be exactly 3 uppercase letters
    - Airport name must be unique
    - IATA code must be unique
    - City must belong to specified country
    
    Used for: POST, PUT, PATCH operations (admin only)
    """
    iata_code = serializers.CharField(
        max_length=3,
        validators=[validate_iata_airport_code]
    )
    
    class Meta:
        model = Airport
        fields = ['name', 'iata_code', 'city', 'country', 'airlines']
    
    def validate(self, data):
        """
        Cross-field validation for Airport.
        
        - City must belong to the specified country
        """
        city = data.get('city')
        country = data.get('country')
        
        if city and country and city.country != country:
            raise serializers.ValidationError(
                "Selected city does not belong to the specified country"
            )
        
        return data
