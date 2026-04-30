"""Country model serializers."""

from rest_framework import serializers
from ..models import Country
from .validators import validate_country_code


class CountryListSerializer(serializers.ModelSerializer):
    """
    Lightweight Country serializer for list views.
    
    Returns essential country information for browsing.
    """
    
    class Meta:
        model = Country
        fields = ['id', 'name', 'code']


class CountryDetailSerializer(serializers.ModelSerializer):
    """
    Complete Country serializer for detail views.
    
    Returns all country information including related cities.
    """
    
    class Meta:
        model = Country
        fields = '__all__'


class CountryCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Country serializer for create and update operations.
    
    Validates:
    - Country code must be exactly 2 uppercase letters (ISO 3166-1 alpha-2)
    - Country name must be unique
    - Country code must be unique
    
    Used for: POST, PUT, PATCH operations (admin only)
    """
    code = serializers.CharField(
        max_length=2,
        validators=[validate_country_code]
    )
    
    class Meta:
        model = Country
        fields = ['name', 'code']
