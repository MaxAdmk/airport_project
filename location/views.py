from rest_framework import viewsets
from core.permissions import IsAdminOrReadOnly
from .models import Country, City
from .serializers import CountrySerializer, CitySerializer

class CountryViewSet(viewsets.ModelViewSet):
    """ViewSet for Country CRUD operations.
    
    Provides endpoints:
    - GET /api/location/countries/ - List all countries (public)
    - POST /api/location/countries/ - Create new country (admins only)
    - GET /api/location/countries/{id}/ - Retrieve country details (public)
    - PUT /api/location/countries/{id}/ - Update country (admins only)
    - DELETE /api/location/countries/{id}/ - Delete country (admins only)
    
    Permission: Authenticated users can read countries. Only admins can create/update/delete.
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAdminOrReadOnly]
    
class CityViewSet(viewsets.ModelViewSet):
    """ViewSet for City CRUD operations.
    
    Provides endpoints:
    - GET /api/location/cities/ - List all cities (public)
    - POST /api/location/cities/ - Create new city (admins only)
    - GET /api/location/cities/{id}/ - Retrieve city details (public)
    - PUT /api/location/cities/{id}/ - Update city (admins only)
    - DELETE /api/location/cities/{id}/ - Delete city (admins only)
    
    Permission: Authenticated users can read cities. Only admins can create/update/delete.
    """
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAdminOrReadOnly]
