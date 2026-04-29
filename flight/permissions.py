from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Permission that allows users to only access objects they own.
    
    For Ticket objects, this means the user must be the passenger.
    Checks the 'passenger' field on the object.
    """
    
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated and request.user.role == 'admin':
            return True
        
        return obj.passenger == request.user


class CanViewOwnTickets(permissions.BasePermission):
    """
    Permission that restricts ticket viewing to:
    - Admins (can view all tickets)
    - Regular users (can only view their own tickets)
    
    Note: This requires the Ticket object to have a 'passenger' field.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Admins can view all tickets
        if request.user.role == 'admin':
            return True
        
        return obj.passenger == request.user


class CanCreateTicket(permissions.BasePermission):
    """
    Permission that restricts ticket creation to authenticated users.
    
    Users can create tickets, but the serializer must validate that 
    the passenger field matches the current user. Admins can create
    tickets for any user.
    
    Note: Object-level validation is enforced in the serializer,
    not in this permission class.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class CanManageTicket(permissions.BasePermission):
    """
    Permission for updating/deleting tickets with admin override.
    
    Rules:
    - Admins can update/delete any ticket
    - Users can only update/delete their own tickets
    - Retrieve and list operations are handled by CanViewOwnTickets
    """
    
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated and request.user.role == 'admin':
            return True
        
        if request.user and request.user.is_authenticated:
            return obj.passenger == request.user
        
        return False
