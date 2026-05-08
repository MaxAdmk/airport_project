from rest_framework import mixins, viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView
from core.permissions import IsAdminOrReadOnly
from flight.filters import FlightFilterSet, TicketFilterSet
from flight.serializers.order import OrderSerializer
from .permissions import CanViewOwnTickets, CanCreateTicket, CanManageTicket
from .models import Flight, Order, Ticket
from .throttling import TicketBookThrottle
from .serializers import (
    FlightListSerializer,
    FlightDetailSerializer,
    FlightCreateUpdateSerializer,
    TicketListSerializer,
    TicketDetailSerializer,
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

class TicketListView(ListAPIView):
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = TicketFilterSet
    ordering_fields = ['id']
    ordering = ['-id']
    
    def get_queryset(self):
        user = self.request.user
        queryset = Ticket.objects.select_related(
            'flight',
            'flight__airline',
            'order',
            'order__customer'
        )

        if user.is_staff:
            return queryset
        elif user.is_authenticated:
            return queryset.filter(order__customer=user)
        else:
            return Ticket.objects.none()
    
    serializer_class = TicketListSerializer
    
class TicketDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return TicketUpdateSerializer
        else:
            return TicketDetailSerializer
    
    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Ticket.objects.select_related('flight')
        return Ticket.objects.filter(order__customer=self.request.user)
    
class OrderViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [TicketBookThrottle]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)
