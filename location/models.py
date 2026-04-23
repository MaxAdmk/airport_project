from django.db import models

class Country(models.Model):
    
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=2, unique=True)
    
    class Meta:
        verbose_name_plural = "Countries"
        
    def __str__(self):
        return self.name
    
class City(models.Model):
    
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='cities')
    
    class Meta:
        verbose_name_plural = "Cities"
        unique_together = ('name', 'country')
        
    def __str__(self):
        return f"{self.name}, {self.country.code}"
