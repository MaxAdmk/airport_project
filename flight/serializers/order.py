from rest_framework import serializers
from django.db import transaction
from flight.models import Ticket, Order

class TicketOrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ('id', 'flight', 'price', 'seat_number', 'baggage_weight','ticket_class', 'passenger_first_name', 'passenger_last_name', 'passenger_passport_code')
        read_only_fields = ('id', 'price')
    
class OrderSerializer(serializers.ModelSerializer):
    
    tickets = TicketOrderItemSerializer(many=True, allow_empty=False)
    
    class Meta:
        model = Order
        fields = ('id', 'tickets', 'created_at')
        
    @transaction.atomic 
    def create(self, validated_data):
        tickets_data = validated_data.pop('tickets')
        order = Order.objects.create(**validated_data)

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
            
        return order