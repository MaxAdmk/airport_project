"""Airport app serializers package."""

from .airline import (
    AirlineListSerializer,
    AirlineDetailSerializer,
    AirlineCreateUpdateSerializer,
)
from .airport import (
    AirportListSerializer,
    AirportDetailSerializer,
    AirportCreateUpdateSerializer,
)
from .airplane import (
    AirplaneListSerializer,
    AirplaneDetailSerializer,
    AirplaneCreateUpdateSerializer,
)

__all__ = [
    'AirlineListSerializer',
    'AirlineDetailSerializer',
    'AirlineCreateUpdateSerializer',
    'AirportListSerializer',
    'AirportDetailSerializer',
    'AirportCreateUpdateSerializer',
    'AirplaneListSerializer',
    'AirplaneDetailSerializer',
    'AirplaneCreateUpdateSerializer',
]
