"""Flight app serializers package."""

from .flight import (
    FlightListSerializer,
    FlightDetailSerializer,
    FlightCreateUpdateSerializer,
)
from .ticket import (
    TicketListSerializer,
    TicketDetailSerializer,
    TicketUpdateSerializer,
)

__all__ = [
    'FlightListSerializer',
    'FlightDetailSerializer',
    'FlightCreateUpdateSerializer',
    'TicketListSerializer',
    'TicketDetailSerializer',
    'TicketUpdateSerializer',
]
