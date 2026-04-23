from django.db import models

from core import settings

class Flight(models.Model):
    
    class Status(models.TextChoices):
        SCHEDULED = 'SCH', 'Scheduled'
        DELAYED = 'DEL', 'Delayed'
        DEPARTED = 'DEP', 'Departed'
        ARRIVED = 'ARR', 'Arrived'
        CANCELLED = 'CAN', 'Cancelled'
    
    flight_number = models.CharField(max_length=10, db_index=True, unique=True)
    departure_airport = models.ForeignKey('airport.Airport', on_delete=models.CASCADE, related_name='departing_flights')
    destination_airport = models.ForeignKey('airport.Airport', on_delete=models.CASCADE, related_name='arriving_flights')
    start_datetime = models.DateTimeField()
    approximate_duration = models.DurationField()
    airplane = models.ForeignKey('airport.Airplane', on_delete=models.SET_NULL, null=True, related_name='flights')
    airline = models.ForeignKey('airport.Airline', on_delete=models.SET_NULL, null=True, related_name='flights')
    status = models.CharField(max_length=3, choices=Status.choices, default=Status.SCHEDULED)
    terminal = models.CharField(max_length=10, null=True, blank=True)
    gate = models.CharField(max_length=10, null=True, blank=True)
    
    def __str__(self):
        return f"{self.flight_number}: {self.departure_airport.iata_code} -> {self.destination_airport.iata_code} ({self.get_status_display()})"
    
class Ticket(models.Model):
    
    class Status(models.TextChoices):
        BOOKED = 'BOK', 'Booked'
        PAID = 'PAI', 'Paid'
        CHECKED_IN = 'CHK', 'Checked-in'
        CANCELLED = 'CAN', 'Cancelled'
    
    class TicketClass(models.TextChoices):
        ECONOMY = 'ECO', 'Economy'
        BUSINESS = 'BUS', 'Business'
        FIRST = 'FIR', 'First Class'
        
    booking_reference = models.CharField(max_length=6, unique=True)
    passenger = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tickets')
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='tickets')
    seat_number = models.CharField(max_length=10)
    ticket_class = models.CharField(max_length=3, choices=TicketClass.choices, default=TicketClass.ECONOMY)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    baggage_weight = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=3, choices=Status.choices, default=Status.BOOKED)
    
    def __str__(self):
        return f"Ticket {self.booking_reference} for {self.passenger} on flight {self.flight.flight_number} ({self.get_status_display()})"