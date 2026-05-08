from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.JWTLoginView.as_view(), name='jwt_login'),
    path('register/', views.JWTRegisterView.as_view(), name='jwt_register'),
    path('refresh/', views.JWTRefreshView.as_view(), name='jwt_refresh'),
    path('logout/', views.JWTLogoutView.as_view(), name='jwt_logout'),
    path('verify/', views.JWTVerifyView.as_view(), name='jwt_verify'),
]