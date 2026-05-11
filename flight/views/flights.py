from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from core.permissions import IsAdminOrReadOnly
from flight.filters import FlightFilterSet
from flight.models import Flight
from flight.serializers import (
    FlightListSerializer,
    FlightDetailSerializer,
    FlightCreateUpdateSerializer,
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
