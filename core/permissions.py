from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Permission that allows access only to users with admin role.
    
    Admins have full access to all resources. Users with role='admin' 
    are considered system administrators.
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role == 'admin'


class CanReadPublic(permissions.BasePermission):
    """
    Permission that allows public read access (GET requests) to all authenticated users.
    
    Write operations (POST, PUT, PATCH, DELETE) are restricted to admins.
    This permission is typically used with IsAdmin for a combined effect:
    - List/Retrieve: Allowed for all authenticated users
    - Create/Update/Delete: Allowed only for admins
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user.role == 'admin'


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission that allows:
    - Read access (GET, HEAD, OPTIONS) to all authenticated users
    - Write access (POST, PUT, PATCH, DELETE) only to admins
    
    Useful for resources like Airports, Airlines, Countries that should be
    readable by everyone but modified only by administrators.
    """
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user.role == 'admin'
