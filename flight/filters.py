from django_filters import FilterSet, CharFilter, DateTimeFilter
from rest_framework import filters as drf_filters
from .models import Flight, Ticket

class FlightFilterSet(FilterSet):
    
    departure_airport_name = CharFilter(
        field_name='departure_airport__name',
        lookup_expr='icontains',
        label='Departure Airport Name'
    )
    
    destination_airport_name = CharFilter(
        field_name='destination_airport__name',
        lookup_expr='icontains',
        label='Destination Airport Name'
    )
    
    departure_after = DateTimeFilter(
        field_name='start_datetime',
        lookup_expr='gte',
        label='Departure After'
    )
    
    departure_before = DateTimeFilter(
        field_name='start_datetime',
        lookup_expr='lte',
        label='Departure Before'
    )
    
    class Meta:
        model = Flight
        fields = ['airline', 'status']

class TicketFilterSet(FilterSet):
    
    class Meta:
        model = Ticket
        fields = ['flight', 'passenger']