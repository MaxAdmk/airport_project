"""User model serializers."""

from rest_framework import serializers
from ..models import User
from .validators import validate_date_of_birth


class UserListSerializer(serializers.ModelSerializer):
    """
    Lightweight User serializer for list views (admin only).
    
    Returns essential user information for admin browsing.
    Only accessible by admins.
    """
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role']


class UserDetailSerializer(serializers.ModelSerializer):
    """
    User serializer for detail views (admin only).
    
    Returns all user information except sensitive auth fields.
    Only accessible by admins.
    Exposes safe fields: email, name, role, passport, citizenship, DOB, phone.
    """
    citizenship_name = serializers.CharField(
        source='citizenship.name',
        read_only=True
    )
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'role',
            'passport_code', 'citizenship', 'citizenship_name',
            'date_of_birth', 'phone_number'
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    """
    User serializer for create operations (admin only).
    
    Validates:
    - Email must be unique
    - Date of birth must be in past and user at least 16 years old
    - Passport code must be unique
    - Password must be strong enough
    
    Used for: POST operations (admin only)
    """
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        help_text="Minimum 8 characters"
    )
    date_of_birth = serializers.DateField(
        validators=[validate_date_of_birth],
        required=False
    )
    
    class Meta:
        model = User
        fields = [
            'email', 'password', 'first_name', 'last_name', 'role',
            'passport_code', 'citizenship', 'date_of_birth', 'phone_number'
        ]
    
    def create(self, validated_data):
        """
        Create user with hashed password.
        """
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
