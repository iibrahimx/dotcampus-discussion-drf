from rest_framework import generics, permissions
from .serializers import SignupSerializer


# Create your views here.
class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]
