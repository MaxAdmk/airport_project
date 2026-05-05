from rest_framework import serializers
from ..models import City


class CityListSerializer(serializers.ModelSerializer):
    """
    Lightweight City serializer for list views.
    
    Returns essential city information for browsing.
    """
    country_name = serializers.CharField(
        source='country.name',
        read_only=True
    )
    
    class Meta:
        model = City
        fields = ['id', 'name', 'country', 'country_name']


class CityDetailSerializer(serializers.ModelSerializer):
    """
    Complete City serializer for detail views.
    
    Returns all city information including related country.
    """
    
    class Meta:
        model = City
        fields = '__all__'


class CityCreateUpdateSerializer(serializers.ModelSerializer):
    """
    City serializer for create and update operations.
    
    Validates:
    - City name must be unique within its country (handled by model Meta)
    - Country must exist
    
    Used for: POST, PUT, PATCH operations (admin only)
    """
    
    class Meta:
        model = City
        fields = ['name', 'country']
