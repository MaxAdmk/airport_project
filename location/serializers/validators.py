import re
from rest_framework import serializers


def validate_country_code(value):
    """
    Validate ISO country code format.
    
    Must be exactly 2 uppercase letters (e.g., US, GB, UA).
    """
    if not re.match(r'^[A-Z]{2}$', value):
        raise serializers.ValidationError(
            "Country code must be exactly 2 uppercase letters"
        )
