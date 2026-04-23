from django.db import models

class Airline(models.Model):
    
    name = models.CharField(max_length=100, unique=True)
    iata_code = models.CharField(max_length=2, unique=True)
    
    def __str__(self):
        return self.name
    
class Airport(models.Model):
    
    name = models.CharField(max_length=255)
    iata_code = models.CharField(max_length=3, unique=True)
    city = models.ForeignKey('location.City', on_delete=models.CASCADE, related_name='airports')
    country = models.ForeignKey('location.Country', on_delete=models.CASCADE, related_name='airports')
    airlines = models.ManyToManyField(Airline, related_name='airports')
    
    def __str__(self):
        return f"{self.name} ({self.iata_code})"
    
class Airplane(models.Model):
    
    model_name = models.CharField(max_length=50)
    tail_number = models.CharField(max_length=20, unique=True)
    num_of_passengers = models.PositiveIntegerField()
    crew_amount = models.PositiveIntegerField()
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE, related_name='airplanes')
    
    def __str__(self):
        return f"{self.model_name} ({self.tail_number})"