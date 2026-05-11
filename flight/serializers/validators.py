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

def validate_seat_existance_in_airplane(seat_number, airplane):
    """
    Validate, does this seat physically exist? (example '12A') 
    inside the airplane.
    """
    if not airplane:
        return
        
    try:
        row_num = int("".join([char for char in seat_number if char.isdigit()]))
        seat_letter = "".join([char for char in seat_number if char.isalpha()]).upper()
        
        if row_num < 1 or row_num > airplane.rows:
            raise serializers.ValidationError(
                f"Row {row_num} does not exist. This airplane only has {airplane.rows} rows."
            )

        valid_letters = airplane.valid_seat_letters
        if seat_letter not in valid_letters:
            raise serializers.ValidationError(
                f"Seat letter '{seat_letter}' is invalid. Valid options for this flight are: {', '.join(valid_letters)}."
            )
            
    except ValueError:
        raise serializers.ValidationError("Invalid seat format. Expected format like '12A'.")