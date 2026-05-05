from rest_framework import viewsets, mixins
from core.permissions import IsAdminOrReadOnly
from .models import Country, City
from .serializers import (
    CountryListSerializer,
    CountryDetailSerializer,
    CountryCreateUpdateSerializer,
    CityListSerializer,
    CityDetailSerializer,
    CityCreateUpdateSerializer,
)

class CountryView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
    ):
    
    queryset = Country.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CountryListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return CountryCreateUpdateSerializer
        return CountryDetailSerializer
    
class CityViewSet(viewsets.ModelViewSet):
    """ViewSet for City CRUD operations.
    
    Provides endpoints:
    - GET /api/location/cities/ - List all cities (public)
    - POST /api/location/cities/ - Create new city (admins only)
    - GET /api/location/cities/{id}/ - Retrieve city details (public)
    - PUT /api/location/cities/{id}/ - Update city (admins only)
    - DELETE /api/location/cities/{id}/ - Delete city (admins only)
    
    Permission: Authenticated users can read cities. Only admins can create/update/delete.
    Serializers vary by action: list/create/detail.
    """
    queryset = City.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return CityListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return CityCreateUpdateSerializer
        return CityDetailSerializer
