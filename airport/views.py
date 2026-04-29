from rest_framework import viewsets
from core.permissions import IsAdminOrReadOnly
from .models import Airline, Airport, Airplane
from .serializers import AirlineSerializer, AirportSerializer, AirplaneSerializer

class AirlineViewSet(viewsets.ModelViewSet):
    """ViewSet for Airline CRUD operations.
    
    Provides endpoints:
    - GET /api/airport/airlines/ - List all airlines (public)
    - POST /api/airport/airlines/ - Create new airline (admins only)
    - GET /api/airport/airlines/{id}/ - Retrieve airline details (public)
    - PUT /api/airport/airlines/{id}/ - Update airline (admins only)
    - DELETE /api/airport/airlines/{id}/ - Delete airline (admins only)
    
    Permission: Authenticated users can read airlines. Only admins can create/update/delete.
    """
    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer
    permission_classes = [IsAdminOrReadOnly]

class AirportViewSet(viewsets.ModelViewSet):
    """ViewSet for Airport CRUD operations.
    
    Provides endpoints:
    - GET /api/airport/airports/ - List all airports (public)
    - POST /api/airport/airports/ - Create new airport (admins only)
    - GET /api/airport/airports/{id}/ - Retrieve airport details (public)
    - PUT /api/airport/airports/{id}/ - Update airport (admins only)
    - DELETE /api/airport/airports/{id}/ - Delete airport (admins only)
    
    Permission: Authenticated users can read airports. Only admins can create/update/delete.
    """
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [IsAdminOrReadOnly]

class AirplaneViewSet(viewsets.ModelViewSet):
    """ViewSet for Airplane CRUD operations.
    
    Provides endpoints:
    - GET /api/airport/airplanes/ - List all airplanes (public)
    - POST /api/airport/airplanes/ - Create new airplane (admins only)
    - GET /api/airport/airplanes/{id}/ - Retrieve airplane details (public)
    - PUT /api/airport/airplanes/{id}/ - Update airplane (admins only)
    - DELETE /api/airport/airplanes/{id}/ - Delete airplane (admins only)
    
    Permission: Authenticated users can read airplanes. Only admins can create/update/delete.
    """
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    permission_classes = [IsAdminOrReadOnly]