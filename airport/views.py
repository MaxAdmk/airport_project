from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Airline, Airport, Airplane
from .serializers import AirlineSerializer, AirportSerializer, AirplaneSerializer

class AirlineViewSet(viewsets.ModelViewSet):
    """ViewSet for Airline CRUD operations.
    
    Provides endpoints:
    - GET /api/airport/airlines/ - List all airlines
    - POST /api/airport/airlines/ - Create new airline
    - GET /api/airport/airlines/{id}/ - Retrieve airline details
    - PUT /api/airport/airlines/{id}/ - Update airline
    - DELETE /api/airport/airlines/{id}/ - Delete airline
    
    TODO: Replace AllowAny with IsAuthenticated and role-based permissions once authorization is fully implemented.
    """
    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer
    permission_classes = [AllowAny]  # TODO: Temporary - replace with IsAuthenticated once auth is implemented

class AirportViewSet(viewsets.ModelViewSet):
    """ViewSet for Airport CRUD operations.
    
    Provides endpoints:
    - GET /api/airport/airports/ - List all airports
    - POST /api/airport/airports/ - Create new airport
    - GET /api/airport/airports/{id}/ - Retrieve airport details
    - PUT /api/airport/airports/{id}/ - Update airport
    - DELETE /api/airport/airports/{id}/ - Delete airport
    
    TODO: Replace AllowAny with IsAuthenticated and role-based permissions once authorization is fully implemented.
    """
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [AllowAny]  # TODO: Temporary - replace with IsAuthenticated once auth is implemented

class AirplaneViewSet(viewsets.ModelViewSet):
    """ViewSet for Airplane CRUD operations.
    
    Provides endpoints:
    - GET /api/airport/airplanes/ - List all airplanes
    - POST /api/airport/airplanes/ - Create new airplane
    - GET /api/airport/airplanes/{id}/ - Retrieve airplane details
    - PUT /api/airport/airplanes/{id}/ - Update airplane
    - DELETE /api/airport/airplanes/{id}/ - Delete airplane
    
    TODO: Replace AllowAny with IsAuthenticated and role-based permissions once authorization is fully implemented.
    """
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    permission_classes = [AllowAny]  # TODO: Temporary - replace with IsAuthenticated once auth is implemented