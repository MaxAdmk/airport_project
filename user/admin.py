from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'passport_code')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'passport_code')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('passport_code', 'role', 'citizenship', 'date_of_birth', 'phone_number')}),
    )
