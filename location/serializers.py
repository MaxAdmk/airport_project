from rest_framework import serializers
from .models import Country, City

class CountrySerializer(serializers.ModelSerializer):
    """Serializer for Country model.
    
    Converts Country model instances to and from JSON.
    Includes country name and ISO country code.
    """
    class Meta:
        model = Country
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    """Serializer for City model.
    
    Converts City model instances to and from JSON.
    Includes city name and country reference.
    """
    class Meta:
        model = City
        fields = '__all__'