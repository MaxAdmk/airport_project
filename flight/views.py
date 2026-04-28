from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Flight, Ticket
from .serializers import FlightSerializer, TicketSerializer

class FlightViewSet(viewsets.ModelViewSet):
    """ViewSet for Flight CRUD operations.
    
    Provides endpoints:
    - GET /api/flight/flights/ - List all flights
    - POST /api/flight/flights/ - Create new flight
    - GET /api/flight/flights/{id}/ - Retrieve flight details
    - PUT /api/flight/flights/{id}/ - Update flight
    - DELETE /api/flight/flights/{id}/ - Delete flight
    
    TODO: Replace AllowAny with IsAuthenticated and role-based permissions once authorization is fully implemented.
    """
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [AllowAny]  # TODO: Temporary - replace with IsAuthenticated once auth is implemented

class TicketViewSet(viewsets.ModelViewSet):
    """ViewSet for Ticket CRUD operations.
    
    Provides endpoints:
    - GET /api/flight/tickets/ - List all tickets
    - POST /api/flight/tickets/ - Create new ticket (booking)
    - GET /api/flight/tickets/{id}/ - Retrieve ticket details
    - PUT /api/flight/tickets/{id}/ - Update ticket
    - DELETE /api/flight/tickets/{id}/ - Delete ticket (cancel)
    
    TODO: Replace AllowAny with IsAuthenticated and role-based permissions once authorization is fully implemented.
    """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [AllowAny]  # TODO: Temporary - replace with IsAuthenticated once auth is implemented