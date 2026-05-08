from django.contrib import admin
from .models import Flight, Ticket, Order

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'departure_airport', 'destination_airport', 'start_datetime', 'status')
    list_filter = ('status', 'departure_airport', 'destination_airport')
    search_fields = ('flight_number',)
    date_hierarchy = 'start_datetime'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('customer__email', 'customer__first_name', 'customer__last_name')
    date_hierarchy = 'created_at'

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'booking_reference', 
        'order', 
        'passenger_first_name', 
        'passenger_last_name',
        'flight',
        'seat_number',
        'status'
    )
    list_filter = ('status', 'ticket_class')
    search_fields = (
        'booking_reference',
        'flight__flight_number',
        'passenger_first_name',
        'passenger_last_name',
        'passenger_passport_code',
        'order__customer__email'
    )
