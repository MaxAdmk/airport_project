from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.contrib.auth import authenticate
from .serializers import LoginSerializer, UserDetailSerializer
from core.throttling import AuthenticationThrottle


class JWTLoginView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AuthenticationThrottle]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'errors': serializer.errors},
                status=HTTP_400_BAD_REQUEST
            )
        
        user = serializer.validated_data['user']
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserDetailSerializer(user).data
        }, status=HTTP_200_OK)


class JWTRefreshView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            
            if not refresh_token:
                return Response(
                    {'error': 'Refresh token required'},
                    status=HTTP_400_BAD_REQUEST
                )
            
            refresh = RefreshToken(refresh_token)
            return Response({
                'access': str(refresh.access_token)
            }, status=HTTP_200_OK)
            
        except (TokenError, InvalidToken):
            return Response(
                {'error': 'Invalid or expired refresh token'},
                status=HTTP_401_UNAUTHORIZED
            )


class JWTLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response({
                'message': 'Successfully logged out'
            }, status=HTTP_200_OK)
            
        except (TokenError, InvalidToken):
            return Response(
                {'error': 'Invalid token'},
                status=HTTP_400_BAD_REQUEST
            )


class JWTVerifyView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            from rest_framework_simplejwt.tokens import Token
            token = Token(request.data.get('token'))
            return Response({'valid': True}, status=HTTP_200_OK)
        except (TokenError, InvalidToken, Exception):
            return Response({'valid': False}, status=HTTP_401_UNAUTHORIZED)
