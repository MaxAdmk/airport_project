from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from core.permissions import IsAdminOrReadOnly
from flight.filters import FlightFilterSet
from flight.models import Flight, Ticket
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
    ordering_fields = ['start_datetime', 'status']
    ordering = ['-start_datetime']
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return FlightListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return FlightCreateUpdateSerializer
        return FlightDetailSerializer

    @action(detail=True, methods=['get'], url_path='available-seats')
    def available_seats(self, request, pk=None):
        flight = self.get_object()
        airplane = flight.airplane

        if not airplane:
            return Response(
                {"detail": "Airplane was not assigned. Seats information is not available."}, 
                status=400
            )

        booked_seats = set(
            Ticket.objects.filter(flight=flight)
            .exclude(status=Ticket.Status.CANCELLED)
            .values_list('seat_number', flat=True)
        )

        valid_letters = airplane.valid_seat_letters
        all_seats = []
        for row in range(1, airplane.rows + 1):
            for letter in valid_letters:
                all_seats.append(f"{row}{letter}")

        available_seats = [seat for seat in all_seats if seat not in booked_seats]

        return Response({
            "flight_number": flight.flight_number,
            "airplane": airplane.tail_number,
            "total_capacity": airplane.rows * airplane.seats_in_row,
            "booked_count": len(booked_seats),
            "available_count": len(available_seats),
            "available_seats": available_seats
        })