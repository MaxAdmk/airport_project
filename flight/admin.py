from django.contrib import admin
from .models import Flight, Ticket

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'departure_airport', 'destination_airport', 'start_datetime', 'status')
    list_filter = ('status', 'departure_airport', 'destination_airport')
    search_fields = ('flight_number',)
    date_hierarchy = 'start_datetime'

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('booking_reference', 'passenger', 'flight', 'seat_number', 'status')
    list_filter = ('status', 'ticket_class')
    search_fields = ('booking_reference', 'passenger__username', 'passenger__last_name', 'flight__flight_number')
