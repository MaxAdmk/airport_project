from rest_framework import viewsets
from core.permissions import IsAdminOrReadOnly
from .permissions import CanViewOwnTickets, CanCreateTicket, CanManageTicket
from .models import Flight, Ticket
from .serializers import FlightSerializer, TicketSerializer

class FlightViewSet(viewsets.ModelViewSet):
    """ViewSet for Flight CRUD operations.
    
    Provides endpoints:
    - GET /api/flight/flights/ - List all flights (public)
    - POST /api/flight/flights/ - Create new flight (admins only)
    - GET /api/flight/flights/{id}/ - Retrieve flight details (public)
    - PUT /api/flight/flights/{id}/ - Update flight (admins only)
    - DELETE /api/flight/flights/{id}/ - Delete flight (admins only)
    
    Permission: Authenticated users can read flights. Only admins can create/update/delete.
    """
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [IsAdminOrReadOnly]

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
    """
    serializer_class = TicketSerializer
    permission_classes = [CanManageTicket, CanViewOwnTickets, CanCreateTicket]
    
    def get_queryset(self):
        if self.request.user and self.request.user.role == 'admin':
            return Ticket.objects.all()
        return Ticket.objects.filter(passenger=self.request.user)