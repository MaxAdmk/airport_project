from rest_framework import viewsets
from core.permissions import IsAdminOrReadOnly
from .permissions import CanViewOwnTickets, CanCreateTicket, CanManageTicket
from .models import Flight, Ticket
from .serializers import (
    FlightListSerializer,
    FlightDetailSerializer,
    FlightCreateUpdateSerializer,
    TicketListSerializer,
    TicketDetailSerializer,
    TicketCreateSerializer,
    TicketUpdateSerializer,
)

class FlightViewSet(viewsets.ModelViewSet):
    """ViewSet for Flight CRUD operations.
    
    Provides endpoints:
    - GET /api/flight/flights/ - List all flights (public)
    - POST /api/flight/flights/ - Create new flight (admins only)
    - GET /api/flight/flights/{id}/ - Retrieve flight details (public)
    - PUT /api/flight/flights/{id}/ - Update flight (admins only)
    - DELETE /api/flight/flights/{id}/ - Delete flight (admins only)
    
    Permission: Authenticated users can read flights. Only admins can create/update/delete.
    Serializers vary by action: list/create/detail.
    """
    queryset = Flight.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return FlightListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return FlightCreateUpdateSerializer
        return FlightDetailSerializer

class TicketViewSet(viewsets.ModelViewSet):
    """ViewSet for Ticket CRUD operations.
    
    Provides endpoints:
    - GET /api/flight/tickets/ - List user's tickets (CanViewOwnTickets)
    - POST /api/flight/tickets/ - Create new ticket (CanCreateTicket)
    - GET /api/flight/tickets/{id}/ - Retrieve ticket details (CanViewOwnTickets)
    - PUT /api/flight/tickets/{id}/ - Update ticket (CanManageTicket)
    - DELETE /api/flight/tickets/{id}/ - Delete/cancel ticket (CanManageTicket)
    
    Permissions:
    - List/Retrieve: Users see only their tickets. Admins see all.
    - Create: Authenticated users can create tickets (serializer validates passenger is user).
    - Update/Delete: Users can manage only their own tickets. Admins can manage all.
    
    Serializers vary by action: list/create/update/detail.
    """
    permission_classes = [CanManageTicket, CanViewOwnTickets, CanCreateTicket]
    
    def get_queryset(self):
        """
        Filter queryset based on user role.
        - Admins see all tickets
        - Regular users see only their own tickets
        """
        if self.request.user and self.request.user.role == 'admin':
            return Ticket.objects.all()
        return Ticket.objects.filter(passenger=self.request.user)
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return TicketListSerializer
        elif self.action == 'create':
            return TicketCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TicketUpdateSerializer
        return TicketDetailSerializer