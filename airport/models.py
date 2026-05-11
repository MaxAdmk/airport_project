import string

from django.db import models

class Airline(models.Model):
    """Represents an airline company.
    
    Attributes:
        name (str): Unique name of the airline.
        iata_code (str): Two-letter IATA code uniquely identifying the airline.
    """
    
    name = models.CharField(max_length=100, unique=True)
    iata_code = models.CharField(max_length=2, unique=True)
    
    def __str__(self):
        return self.name
    
class Airport(models.Model):
    """Represents an airport.
    
    Attributes:
        name (str): Name of the airport.
        iata_code (str): Three-letter IATA code uniquely identifying the airport.
        city (ForeignKey): Reference to the City where the airport is located.
        country (ForeignKey): Reference to the Country where the airport is located.
        airlines (ManyToMany): Airlines operating from this airport.
    """
    
    name = models.CharField(max_length=255)
    iata_code = models.CharField(max_length=3, unique=True)
    city = models.ForeignKey('location.City', on_delete=models.CASCADE, related_name='airports')
    country = models.ForeignKey('location.Country', on_delete=models.CASCADE, related_name='airports')
    airlines = models.ManyToManyField(Airline, related_name='airports')
    
    def __str__(self):
        return f"{self.name} ({self.iata_code})"
    
class Airplane(models.Model):
    """Represents a physical aircraft.
    
    Attributes:
        model_name (str): Aircraft model (e.g., Boeing 737).
        tail_number (str): Unique aircraft registration number.
        rows (int): Number of seat rows.
        seats_in_row (int): Number of seats per row.
        crew_amount (int): Required number of crew members.
        airline (ForeignKey): Airline that owns this aircraft.
    """
    
    model_name = models.CharField(max_length=50)
    tail_number = models.CharField(max_length=20, unique=True)
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()
    crew_amount = models.PositiveIntegerField()
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE, related_name='airplanes')
    
    def __str__(self):
        return f"{self.model_name} ({self.tail_number})"
    
    @property
    def valid_seat_letters(self):
        return list(string.ascii_uppercase[:self.seats_in_row])
    
    @property
    def num_of_passengers(self):
        """Calculates total passenger capacity based on rows and seats."""
        return self.rows * self.seats_in_row