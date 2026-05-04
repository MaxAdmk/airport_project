from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from core.permissions import IsAdminOrReadOnly
from flight.filters import FlightFilterSet, TicketFilterSet
from .permissions import CanViewOwnTickets, CanCreateTicket, CanManageTicket
from .models import Flight, Ticket
from .throttling import TicketBookThrottle
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
    
    queryset = Flight.objects.select_related(
        'airline', 'departure_airport', 'destination_airport'
    )
    permission_classes = [IsAdminOrReadOnly]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = FlightFilterSet
    search_fields = ['airline__name', 'departure_airport__name', 'destination_airport__name']
    ordering_fields = ['departure_time', 'arrival_time', 'status']
    ordering = ['-departure_time']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return FlightListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return FlightCreateUpdateSerializer
        return FlightDetailSerializer

class TicketListCreateView(ListCreateAPIView):
    permission_classes = [CanViewOwnTickets, CanCreateTicket]
    throttle_classes = [TicketBookThrottle]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = TicketFilterSet
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        if self.request.user and self.request.user.role == 'admin':
            return Ticket.objects.select_related('flight', 'passenger')
        return Ticket.objects.filter(passenger=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TicketCreateSerializer
        return TicketListSerializer
    
class TicketDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [CanManageTicket]
    
    def get_queryset(self):
        if self.request.user and self.request.user.role == 'admin':
            return Ticket.objects.select_related('flight', 'passenger')
        return Ticket.objects.filter(passenger=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return TicketUpdateSerializer
        return TicketDetailSerializer