from rest_framework import viewsets
from core.permissions import IsAdminOrReadOnly
from .models import Airline, Airport, Airplane
from .serializers import (
    AirlineListSerializer,
    AirlineDetailSerializer,
    AirlineCreateUpdateSerializer,
    AirportListSerializer,
    AirportDetailSerializer,
    AirportCreateUpdateSerializer,
    AirplaneListSerializer,
    AirplaneDetailSerializer,
    AirplaneCreateUpdateSerializer,
)


class AirlineViewSet(viewsets.ModelViewSet):
    """ViewSet for Airline CRUD operations.
    
    Provides endpoints:
    - GET /api/airport/airlines/ - List all airlines (public)
    - POST /api/airport/airlines/ - Create new airline (admins only)
    - GET /api/airport/airlines/{id}/ - Retrieve airline details (public)
    - PUT /api/airport/airlines/{id}/ - Update airline (admins only)
    - DELETE /api/airport/airlines/{id}/ - Delete airline (admins only)
    
    Permission: Authenticated users can read airlines. Only admins can create/update/delete.
    Serializers vary by action: list/create/detail.
    """
    queryset = Airline.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return AirlineListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return AirlineCreateUpdateSerializer
        return AirlineDetailSerializer


class AirportViewSet(viewsets.ModelViewSet):
    """ViewSet for Airport CRUD operations.
    
    Provides endpoints:
    - GET /api/airport/airports/ - List all airports (public)
    - POST /api/airport/airports/ - Create new airport (admins only)
    - GET /api/airport/airports/{id}/ - Retrieve airport details (public)
    - PUT /api/airport/airports/{id}/ - Update airport (admins only)
    - DELETE /api/airport/airports/{id}/ - Delete airport (admins only)
    
    Permission: Authenticated users can read airports. Only admins can create/update/delete.
    Serializers vary by action: list/create/detail.
    """
    queryset = Airport.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return AirportListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return AirportCreateUpdateSerializer
        return AirportDetailSerializer


class AirplaneViewSet(viewsets.ModelViewSet):
    """ViewSet for Airplane CRUD operations.
    
    Provides endpoints:
    - GET /api/airport/airplanes/ - List all airplanes (public)
    - POST /api/airport/airplanes/ - Create new airplane (admins only)
    - GET /api/airport/airplanes/{id}/ - Retrieve airplane details (public)
    - PUT /api/airport/airplanes/{id}/ - Update airplane (admins only)
    - DELETE /api/airport/airplanes/{id}/ - Delete airplane (admins only)
    
    Permission: Authenticated users can read airplanes. Only admins can create/update/delete.
    Serializers vary by action: list/create/detail.
    """
    queryset = Airplane.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return AirplaneListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return AirplaneCreateUpdateSerializer
        return AirplaneDetailSerializer