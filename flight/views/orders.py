from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from flight.models import Order
from flight.serializers.order import OrderSerializer
from flight.throttling import TicketBookThrottle


class OrderViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [TicketBookThrottle]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)
