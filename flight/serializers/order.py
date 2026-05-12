from rest_framework import serializers
from django.db import transaction, IntegrityError
from flight.models import Ticket, Order
from .validators import validate_seat_number_format, validate_future_datetime, validate_seat_existance_in_airplane

class TicketOrderItemSerializer(serializers.ModelSerializer):

    seat_number = serializers.CharField(
        max_length = 10,
        validators = [validate_seat_number_format]
    )
    baggage_weight = serializers.IntegerField(
        min_value=0,
        max_value=100,
        default=0
    )

    class Meta:
        model = Ticket
        fields = ('id', 'flight', 'price', 'seat_number', 'baggage_weight','ticket_class', 'passenger_first_name', 'passenger_last_name', 'passenger_passport_code')
        read_only_fields = ('id', 'price')
        validators = []
        
    def validate(self, data):
        flight = data['flight']
        seat = data['seat_number']
        
        validate_future_datetime(flight.start_datetime)
        
        validate_seat_existance_in_airplane(seat, flight.airplane)
        
        seat_taken = Ticket.objects.filter(
            flight=flight,
            seat_number=seat
        ).exclude(
            status__in=[Ticket.Status.CANCELLED]
        ).exists()
        
        if seat_taken:
            raise serializers.ValidationError(f"Seat {seat} at flight:{flight.flight_number} , is already taken")
        
        return data
    
class OrderSerializer(serializers.ModelSerializer):
    
    tickets = TicketOrderItemSerializer(many=True, allow_empty=False)
    
    class Meta:
        model = Order
        fields = ('id', 'tickets', 'created_at')
    
    def validate(self, data):
        tickets_data = data.get('tickets', [])
        seen_seats = set()
        
        for ticket in tickets_data:
            flight = ticket['flight']
            seat = ticket['seat_number']
            identifier = f"{flight.id}-{seat}"
            
            if identifier in seen_seats:
                raise serializers.ValidationError(
                    f"You are trying to book seat {seat} at the flight {flight.flight_number} more than once."
                )
            seen_seats.add(identifier)
        
        return data
    
    @transaction.atomic 
    def create(self, validated_data):
        tickets_data = validated_data.pop('tickets')
        order = Order.objects.create(**validated_data)

        try: 
            for ticket_data in tickets_data:
                flight = ticket_data['flight']
                ticket_class = ticket_data.get('ticket_class', Ticket.TicketClass.ECONOMY)
            
                if ticket_class == Ticket.TicketClass.ECONOMY:
                    actual_price = flight.price_economy
                elif ticket_class == Ticket.TicketClass.BUSINESS:
                    actual_price = flight.price_business
                elif ticket_class == Ticket.TicketClass.FIRST:
                    actual_price = flight.price_first_class
                else:
                    actual_price = flight.price_economy  
            
                Ticket.objects.create(
                    order=order,
                    price=actual_price,
                    **ticket_data
                )
        except IntegrityError:
            raise serializers.ValidationError(
                {'detail': 'One or more selected seats were just booked by someone else. Please choose different seats.'}
            )    
        
        return order
