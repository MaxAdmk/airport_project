from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User CRUD operations.
    
    Provides endpoints:
    - GET /api/user/users/ - List all users
    - POST /api/user/users/ - Create new user
    - GET /api/user/users/{id}/ - Retrieve user details
    - PUT /api/user/users/{id}/ - Update user
    - DELETE /api/user/users/{id}/ - Delete user
    
    TODO: Replace AllowAny with IsAuthenticated and role-based permissions once authorization is fully implemented.
    Only exposes safe user fields (excludes passwords, emails, passport codes).
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # TODO: Temporary - replace with IsAuthenticated once auth is implemented