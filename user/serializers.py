from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model.
    
    Converts User model instances to and from JSON.
    Exposes only safe fields: id, username, first_name, last_name, role, date_of_birth, phone_number.
    Excludes sensitive fields: password, email, passport_code, citizenship.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'role', 'date_of_birth', 'phone_number')
        read_only_fields = ('id',) 