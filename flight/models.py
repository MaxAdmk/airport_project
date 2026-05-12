from django.db import models
from django.db.models import Q
from django.utils import timezone
import uuid
import string
import random

from core import settings


def generate_booking_reference():
    """
    Generate a unique 6-character booking reference.
    Format: 3 uppercase letters + 3 digits
    Example: ABC123
    """
    letters = ''.join(random.choices(string.ascii_uppercase, k=3))
    digits = ''.join(random.choices(string.digits, k=3))
    return letters + digits

class Flight(models.Model):
    """Represents a scheduled flight.
    
    Attributes:
        flight_number (str): Unique flight identifier code.
        departure_airport (ForeignKey): Originating airport.
        destination_airport (ForeignKey): Destination airport.
        start_datetime (DateTime): Scheduled departure time.
        approximate_duration (Duration): Expected flight duration.
        airplane (ForeignKey): Aircraft assigned to this flight (nullable).
        airline (ForeignKey): Operating airline (nullable).
        status (str): Current flight status (Scheduled, Delayed, Departed, Arrived, Cancelled).
        terminal (str): Departure terminal code (optional).
        gate (str): Departure gate number (optional).
    """
    
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
    price_economy = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)
    price_business = models.DecimalField(max_digits=10, decimal_places=2, default=250.00)
    price_first_class = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)
    
    def __str__(self):
        return f"{self.flight_number}: {self.departure_airport.iata_code} -> {self.destination_airport.iata_code} ({self.get_status_display()})"
    
    @property
    def arrival_datetime(self):
        """Calculate estimated arrival time from departure + duration."""
        return self.start_datetime + self.approximate_duration
    
class Order(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    
    def __str__(self):
        status = "Paid" if self.is_paid else "Pending"
        return f"Order {self.id} by {self.customer.email} ({status})"

class Ticket(models.Model):
    """Represents a flight ticket/booking for a passenger.
    
    Attributes:
        booking_reference (str): Unique 6-character booking confirmation code.
        passenger_first_name (str): First name of the passenger.
        passenger_last_name (str): Last name of the passenger.
        passenger_passport_code (str): Passport code of the passenger.
        flight (ForeignKey): Associated flight.
        seat_number (str): Assigned seat (e.g., 12A).
        ticket_class (str): Cabin class (Economy, Business, First Class).
        price (Decimal): Ticket price in currency units.
        baggage_weight (int): Allowed baggage weight in kg.
        status (str): Ticket status (Booked, Paid, Checked-in, Cancelled).
    """
    
    class Status(models.TextChoices):
        BOOKED = 'BOK', 'Booked'
        PAID = 'PAI', 'Paid'
        CHECKED_IN = 'CHK', 'Checked-in'
        CANCELLED = 'CAN', 'Cancelled'
    
    class TicketClass(models.TextChoices):
        ECONOMY = 'ECO', 'Economy'
        BUSINESS = 'BUS', 'Business'
        FIRST = 'FIR', 'First Class'
        
    booking_reference = models.CharField(
        max_length=6,
        unique=True,
        default=generate_booking_reference,
        editable=False,
        db_index=True,
        help_text="Auto-generated 6-character booking reference (e.g., ABC123)"
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='tickets')
    passenger_first_name = models.CharField(max_length=50)
    passenger_last_name = models.CharField(max_length=50)
    passenger_passport_code = models.CharField(max_length=20)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='tickets')
    seat_number = models.CharField(max_length=10)
    ticket_class = models.CharField(max_length=3, choices=TicketClass.choices, default=TicketClass.ECONOMY)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    baggage_weight = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=3, choices=Status.choices, default=Status.BOOKED)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['flight', 'seat_number'],
                condition=~Q(status__in=['CAN']),
                name = 'unique_seat_per_flight'
            )
        ]
    
    def __str__(self):
        return f"Ticket {self.booking_reference} for {self.passenger_first_name} {self.passenger_last_name} on flight {self.flight.flight_number} ({self.get_status_display()})"