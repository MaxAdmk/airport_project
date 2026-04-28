from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Country, City
from .serializers import CountrySerializer, CitySerializer

class CountryViewSet(viewsets.ModelViewSet):
    """ViewSet for Country CRUD operations.
    
    Provides endpoints:
    - GET /api/location/countries/ - List all countries
    - POST /api/location/countries/ - Create new country
    - GET /api/location/countries/{id}/ - Retrieve country details
    - PUT /api/location/countries/{id}/ - Update country
    - DELETE /api/location/countries/{id}/ - Delete country
    
    TODO: Replace AllowAny with IsAuthenticated and role-based permissions once authorization is fully implemented.
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [AllowAny]  # TODO: Temporary - replace with IsAuthenticated once auth is implemented
    
class CityViewSet(viewsets.ModelViewSet):
    """ViewSet for City CRUD operations.
    
    Provides endpoints:
    - GET /api/location/cities/ - List all cities
    - POST /api/location/cities/ - Create new city
    - GET /api/location/cities/{id}/ - Retrieve city details
    - PUT /api/location/cities/{id}/ - Update city
    - DELETE /api/location/cities/{id}/ - Delete city
    
    TODO: Replace AllowAny with IsAuthenticated and role-based permissions once authorization is fully implemented.
    """
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [AllowAny]  # TODO: Temporary - replace with IsAuthenticated once auth is implemented
