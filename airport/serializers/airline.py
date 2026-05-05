from rest_framework import serializers
from ..models import Airline
from .validators import validate_iata_airline_code


class AirlineListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airline
        fields = ['id', 'name', 'iata_code']


class AirlineDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airline
        fields = '__all__'


class AirlineCreateUpdateSerializer(serializers.ModelSerializer):
    iata_code = serializers.CharField(
        max_length=2,
        validators=[validate_iata_airline_code]
    )
    
    class Meta:
        model = Airline
        fields = ['name', 'iata_code']
