from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from .models import User, HospitalProfile, VendorProfile
from .permissions import IsUserOrReadOnly
from .serializers import CreateUserSerializer, CreateHospitalSerializer, CreateVendorSerializer, UserSerializer


class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    Updates and retrieves user accounts
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUserOrReadOnly,)



class UserCreateViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """
    Creates user accounts
    """
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)

class HospitalCreateViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """
    Creates user accounts
    """
    queryset = HospitalProfile.objects.all()
    serializer_class = CreateHospitalSerializer
    permission_classes = (AllowAny,)

class VendorCreateViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """
    Creates user accounts
    """
    queryset = VendorProfile.objects.all()
    serializer_class = CreateVendorSerializer
    permission_classes = (AllowAny,)
