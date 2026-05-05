"""Flight app serializers package."""

from .flight import (
    FlightListSerializer,
    FlightDetailSerializer,
    FlightCreateUpdateSerializer,
)
from .ticket import (
    TicketListSerializer,
    TicketDetailSerializer,
    TicketCreateSerializer,
    TicketUpdateSerializer,
)

__all__ = [
    'FlightListSerializer',
    'FlightDetailSerializer',
    'FlightCreateUpdateSerializer',
    'TicketListSerializer',
    'TicketDetailSerializer',
    'TicketCreateSerializer',
    'TicketUpdateSerializer',
]
