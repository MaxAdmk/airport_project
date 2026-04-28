from django.contrib import admin
from .models import Airline, Airport, Airplane

@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):
    list_display = ('name', 'iata_code')
    search_fields = ('name', 'iata_code')

@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ('name', 'iata_code', 'city', 'country')
    list_filter = ('country',)
    search_fields = ('name', 'iata_code', 'city')

@admin.register(Airplane)
class AirplaneAdmin(admin.ModelAdmin):
    list_display = ('tail_number', 'model_name', 'airline', 'num_of_passengers')
    list_filter = ('airline',)
    search_fields = ('tail_number', 'model_name')