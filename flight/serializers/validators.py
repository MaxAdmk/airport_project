import re
from django.utils import timezone
from rest_framework import serializers


def validate_seat_number_format(value):
    """
    Validate seat number format.
    
    Seat must be 1-3 digits followed by a capital letter.
    """
    if not re.match(r'^\d{1,3}[A-Z]$', value):
        raise serializers.ValidationError(
            "Seat must be format like '12A' (1-3 digits followed by capital letter)"
        )


def validate_future_datetime(value):
    """
    Validate that datetime is in the future.
    """
    if value < timezone.now():
        raise serializers.ValidationError(
            "Flight date and time must be in the future"
        )


def validate_positive_duration(value):
    """
    Validate that duration is positive.
    """
    if value.total_seconds() <= 0:
        raise serializers.ValidationError(
            "Flight duration must be greater than zero"
        )
