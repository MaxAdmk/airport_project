from datetime import date
from rest_framework import serializers


def validate_date_of_birth(value):
    """
    Validate date of birth is in the past and user is at least 16 years old.
    """
    today = date.today()
    
    if value >= today:
        raise serializers.ValidationError(
            "Date of birth must be in the past"
        )
    
    # Calculate age
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    
    if age < 16:
        raise serializers.ValidationError(
            "User must be at least 16 years old"
        )
