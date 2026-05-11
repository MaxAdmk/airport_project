import stripe
import logging
from django.conf import settings
from django.http import HttpResponse
from rest_framework.views import APIView, csrf_exempt
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.core.mail import send_mail
from ..models import Order, Ticket

stripe.api_key = settings.STRIPE_SECRET_KEY
logger = logging.getLogger(__name__)

class CreateStripeCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, customer=request.user)
        
        if order.is_paid:
            return Response({"detail": "This order is already paid."}, status=400)

        line_items = []
        
        for ticket in order.tickets.all():
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(ticket.price * 100),
                    'product_data': {
                        'name': f"Flight {ticket.flight.flight_number} (Seat {ticket.seat_number})",
                        'description': f"Passanger: {ticket.passenger_first_name} {ticket.passenger_last_name} | Ticket Class: {ticket.get_ticket_class_display()}",
                    },
                },
                'quantity': 1,
            })

        DOMAIN = settings.BASE_URL

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=DOMAIN + '/api/flight/success/',
                cancel_url=DOMAIN + '/api/flight/cancel/',
                client_reference_id=str(order.id) 
            )

            return Response({'checkout_url': checkout_session.url})
            
        except Exception as e:
            return Response({'error': str(e)}, status=500)
        
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        # Check Stripe signature
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse("Invalid payload", status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse("Invalid signature", status=400)

    # If payment is successfull
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        order_id = session.client_reference_id
        
        if order_id:
            try:
                # Open transaction: update Order and Tickets together
                with transaction.atomic():
                    order = Order.objects.get(id=order_id)
                    order.is_paid = True
                    order.save()
                    
                    # Bulk update of ticket payment statuses
                    order.tickets.update(status=Ticket.Status.PAID)
                    
                    logger.info(f"Success! Order {order_id} and the tickets were updated to PAID.")
                    
                    # Email part
                    customer_email = order.customer.email
                    tickets = order.tickets.all()
                    
                    subject = f"Payment Confirmation: Flight Tickets (Order #{order.id})"
                    
                    message = "Dear Passenger,\n\nYour payment was successfully processed. Here are your ticket details:\n\n"
                    for t in tickets:
                        message += f"- Flight: {t.flight.flight_number} | Seat: {t.seat_number} | Passenger: {t.passenger_first_name} {t.passenger_last_name}\n"
                    
                    message += "\nWe wish you a safe and pleasant flight!\nBest regards,\nThe Airport Team"
                    
                    try:
                        sent_count = send_mail(
                            subject=subject,
                            message=message,
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[customer_email],
                            fail_silently=False,
                        )
                        
                        if sent_count > 0:
                            logger.info(f"Email successfully sent to {customer_email}. Status code: {sent_count}")
                        else:
                            logger.warning(f"Email to {customer_email} was not sent. Status code: {sent_count}")
                            
                    except Exception as e:
                        logger.error(f"Failed to send email to {customer_email}. Error: {str(e)}")
                    
            except Order.DoesNotExist:
                logger.error(f"Error: Order with ID {order_id} was not found in DB.")

    return HttpResponse(status=200)

class PaymentSuccessView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response({"message": "Payment success! Your tickets are submitted."})

class PaymentCancelView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return Response({"message": "Payment canceled. You can try once more later."})