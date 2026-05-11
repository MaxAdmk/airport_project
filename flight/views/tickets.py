from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from flight.filters import TicketFilterSet
from flight.models import Ticket
from flight.serializers import (
    TicketListSerializer,
    TicketDetailSerializer,
    TicketUpdateSerializer,
)
from flight.permissions import CanViewOwnTickets, CanCreateTicket, CanManageTicket


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
