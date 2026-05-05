"""Location app serializers package."""

from .country import (
    CountryListSerializer,
    CountryDetailSerializer,
    CountryCreateUpdateSerializer,
)
from .city import (
    CityListSerializer,
    CityDetailSerializer,
    CityCreateUpdateSerializer,
)

__all__ = [
    'CountryListSerializer',
    'CountryDetailSerializer',
    'CountryCreateUpdateSerializer',
    'CityListSerializer',
    'CityDetailSerializer',
    'CityCreateUpdateSerializer',
]
