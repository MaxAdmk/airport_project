from rest_framework.throttling import UserRateThrottle

class TicketBookThrottle(UserRateThrottle):
    scope = 'ticket_book'