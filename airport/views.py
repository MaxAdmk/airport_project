from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from core.permissions import IsAdminOrReadOnly
from .models import Airline, Airport, Airplane
from .serializers import (
    AirlineListSerializer,
    AirlineDetailSerializer,
    AirlineCreateUpdateSerializer,
    AirportListSerializer,
    AirportDetailSerializer,
    AirportCreateUpdateSerializer,
    AirplaneListSerializer,
    AirplaneDetailSerializer,
    AirplaneCreateUpdateSerializer,
)


class AirlineListCreateView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request):
        airlines = Airline.objects.all()
        serializer = AirlineListSerializer(airlines, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        if not request.user.is_authenticated or request.user.role != 'admin':
            return Response({'detail': 'Only admins can create airlines.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = AirlineCreateUpdateSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AirlineDetailView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get_object(self, pk):
        try:
            return Airline.objects.get(pk=pk)
        except Airline.DoesNotExist:
            return None
        
    def get(self, request, pk):
        airline = self.get_object(pk)
        if not airline:
            return Response({'detail': 'Airline not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = AirlineDetailSerializer(airline)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        if not request.user.is_authenticated or request.user.role != 'admin':
            return Response({'detail': 'Only admins can update airlines.'}, status=status.HTTP_403_FORBIDDEN)

        airline=self.get_object(pk)
        if not airline:
            return Response({'detail': 'Airline not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = AirlineCreateUpdateSerializer(airline, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request, pk):
        if not request.user.is_authenticated or request.user.role != 'admin':
            return Response({'detail': 'Only admins can delete airlines.'}, status=status.HTTP_403_FORBIDDEN)

        airline = self.get_object(pk)
        if not airline:
            return Response({'detail': 'Airline not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        airline.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AirportViewSet(viewsets.ModelViewSet):
    """ViewSet for Airport CRUD operations.
    
    Provides endpoints:
    - GET /api/airport/airports/ - List all airports (public)
    - POST /api/airport/airports/ - Create new airport (admins only)
    - GET /api/airport/airports/{id}/ - Retrieve airport details (public)
    - PUT /api/airport/airports/{id}/ - Update airport (admins only)
    - DELETE /api/airport/airports/{id}/ - Delete airport (admins only)
    
    Permission: Authenticated users can read airports. Only admins can create/update/delete.
    Serializers vary by action: list/create/detail.
    """
    queryset = Airport.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return AirportListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return AirportCreateUpdateSerializer
        return AirportDetailSerializer


class AirplaneViewSet(viewsets.ModelViewSet):
    """ViewSet for Airplane CRUD operations.
    
    Provides endpoints:
    - GET /api/airport/airplanes/ - List all airplanes (public)
    - POST /api/airport/airplanes/ - Create new airplane (admins only)
    - GET /api/airport/airplanes/{id}/ - Retrieve airplane details (public)
    - PUT /api/airport/airplanes/{id}/ - Update airplane (admins only)
    - DELETE /api/airport/airplanes/{id}/ - Delete airplane (admins only)
    
    Permission: Authenticated users can read airplanes. Only admins can create/update/delete.
    Serializers vary by action: list/create/detail.
    """
    queryset = Airplane.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return AirplaneListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return AirplaneCreateUpdateSerializer
        return AirplaneDetailSerializer