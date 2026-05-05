from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'airports', views.AirportViewSet)
router.register(r'airplanes', views.AirplaneViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('airlines/', views.AirlineListCreateView.as_view(), name='airline-list-create'),
    path('airlines/<int:pk>/', views.AirlineDetailView.as_view(), name='airline-detail'),
]