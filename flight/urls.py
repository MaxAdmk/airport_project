from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'flights', views.FlightViewSet)
router.register(r'orders', views.OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('tickets/', views.TicketListView.as_view(), name='ticket-list'),
    path('tickets/<int:pk>/', views.TicketDetailView.as_view(), name='ticket-detail'),
    path('orders/<int:order_id>/checkout/', views.CreateStripeCheckoutSessionView.as_view(), name='order-checkout'),
    path('webhook/', views.stripe_webhook, name='stripe-webhook'),
    path('success/', views.PaymentSuccessView.as_view(), name='payment-success'),
    path('cancel/', views.PaymentCancelView.as_view(), name='payment-cancel'),
]