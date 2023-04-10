from rest_framework import generics
from .models import Property, Investment, Crop
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .permissions import IsOwnerOrAdmin, IsAdminOrReadOnly
from .serializers import PropertySerializer, InvestmentSerializer, CropSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken



class PropertyListCreate(generics.ListCreateAPIView):
    queryset = Property.objects.all().order_by('property_type')
    serializer_class = PropertySerializer
    permission_classes = [IsAdminOrReadOnly]

class PropertyDetail(generics.RetrieveAPIView):  # Add this class for the property detail view
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class InvestmentListCreate(generics.ListCreateAPIView):
    queryset = Investment.objects.select_related('property', 'investor').order_by('property')
    serializer_class = InvestmentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    # should only list investments for the logged in user
    def get_queryset(self):
        return self.queryset.filter(investor=self.request.user)


class InvestmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Investment.objects.select_related('property', 'investor')
    serializer_class = InvestmentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

class CropListCreate(generics.ListCreateAPIView):
    queryset = Crop.objects.all().order_by('name')
    serializer_class = CropSerializer
    permission_classes = [IsAdminOrReadOnly]

class CropDetail(generics.RetrieveAPIView):  # Add this class for the crop detail view
    queryset = Crop.objects.all()
    serializer_class = CropSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class RegisterView(APIView):
    """Register a new user."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_409_CONFLICT)

        user = User(username=username)
        user.set_password(password)
        user.save()

        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    """Login a user and return an access token."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({'access': access_token})
