from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AirlineViewSet, AirportViewSet, AirplaneViewSet

router = DefaultRouter()
router.register(r'airlines', AirlineViewSet)
router.register(r'airports', AirportViewSet)
router.register(r'airplanes', AirplaneViewSet)

urlpatterns = [
    path('', include(router.urls)),
]