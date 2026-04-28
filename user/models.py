from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Custom user model extending Django's AbstractUser.
    
    Attributes:
        passport_code (str): Unique passport identification number.
        role (str): User role (Admin or User).
        citizenship (ForeignKey): User's country of citizenship.
        date_of_birth (Date): User's birth date (optional).
        phone_number (str): Contact phone number (optional).
        
    Note:
        Inherits username, email, password, first_name, last_name from AbstractUser.
    """
    
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        USER = 'user', 'User'
    
    passport_code = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.USER)
    citizenship = models.ForeignKey('location.Country', on_delete=models.SET_NULL, null=True, related_name='citizens')
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_role_display()})"
