from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
class RegisterView(APIView):
    permission_classes=[permissions.AllowAny]
    def post(self, request, version):
        s=RegisterSerializer(data=request.data); s.is_valid(raise_exception=True)
        u=s.save(); return Response(UserSerializer(u).data, status=status.HTTP_201_CREATED)
class LoginView(APIView):
    permission_classes=[permissions.AllowAny]
    def post(self, request, version):
        s=LoginSerializer(data=request.data); s.is_valid(raise_exception=True)
        u=s.validated_data['user']; r=RefreshToken.for_user(u)
        return Response({'access':str(r.access_token),'refresh':str(r),'user':UserSerializer(u).data})
class MeView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get(self, request, version):
        return Response(UserSerializer(request.user).data)
    def patch(self, request, version):
        s=UserSerializer(request.user, data=request.data, partial=True)
        s.is_valid(raise_exception=True); s.save(); return Response(s.data)
