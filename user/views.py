from rest_framework import viewsets
from core.permissions import IsAdmin
from .models import User
from .serializers import (
    UserListSerializer,
    UserDetailSerializer,
    UserCreateSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User CRUD operations.
    
    Provides endpoints:
    - GET /api/user/users/ - List all users (admins only)
    - POST /api/user/users/ - Create new user (admins only)
    - GET /api/user/users/{id}/ - Retrieve user details (admins only)
    - PUT /api/user/users/{id}/ - Update user (admins only)
    - DELETE /api/user/users/{id}/ - Delete user (admins only)
    
    Permission: Only admins can access user data. This protects sensitive user information.
    Only exposes safe user fields.
    For password changes, use /api/auth/password-change/ endpoint.
    
    Serializers vary by action: list/create/detail.
    """
    queryset = User.objects.all()
    permission_classes = [IsAdmin]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return UserListSerializer
        elif self.action == 'create':
            return UserCreateSerializer
        return UserDetailSerializer