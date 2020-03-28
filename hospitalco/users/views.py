from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets, mixins, views
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import authenticate, SessionAuthentication, BasicAuthentication 
from rest_framework.response import Response
from .models import User, HospitalProfile, VendorProfile, Item, Category, Requirement, Stock
from .permissions import IsUserOrReadOnly
from .serializers import CreateUserSerializer, UserSerializer, HospitalProfileSerializer, \
    VendorProfileSerializer, CreateHospitalSerializer, CreateVendorSerializer, CreateRequirementSerializer, \
    CreateStockSerializer, ItemSerializer, CategorySerializer, StockSerializer, RequirementSerializer


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

class UserRegisterViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """
    Registers user accounts
    """

    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)

class UserDetailsView(views.APIView):
    """
    Returns current authenticated user's information
    """

    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def get(self, request):

        user = request.user

        return Response(UserSerializer(user).data)

class UserLoginView(views.APIView):
    """
    Logs in a user
    """

    permission_classes = (AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request):
        
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class UserLogoutView(views.APIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def get(self, request):

        logout(request)
        
        return Response(status=status.HTTP_200_OK)

class UserListSet(mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """
    Updates and retrieves user accounts
    """
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

class HospitalViewSet(mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """
    Updates and retrieves user accounts
    """
    
    queryset = HospitalProfile.objects.all()
    serializer_class = HospitalProfileSerializer
    permission_classes = (AllowAny,)

class VendorViewSet(mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """
    Updates and retrieves user accounts
    """
    
    queryset = VendorProfile.objects.all()
    serializer_class = VendorProfileSerializer
    permission_classes = (AllowAny,)

class UserHospitalView(viewsets.ViewSet):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def get(self, request):

        try:
            queryset = HospitalProfile.objects.get(user=request.user)
            serializer = HospitalProfileSerializer(queryset)
            return Response(serializer.data)

        except HospitalProfile.DoesNotExist:
            return Response(status=status.HTTP_200_OK)

    def post(self, request):

        serializer = CreateHospitalSerializer(data=request.data, context={'user': request.user})
        if not serializer.is_valid():
            return Response(serializer.errors)
        serializer.save()

        return Response(serializer.data)

class UserVendorView(viewsets.ViewSet):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def get(self, request):

        try:
            queryset = VendorProfile.objects.get(user=request.user)
            serializer = VendorProfileSerializer(queryset)
            return Response(serializer.data)

        except VendorProfile.DoesNotExist:
            return Response(status=status.HTTP_200_OK)

    def post(self, request):

        serializer = CreateVendorSerializer(data=request.data, context={'user': request.user})
        if not serializer.is_valid():
            return Response(serializer.errors)
        serializer.save()

        return Response(serializer.data)
    
class HospitalRequirementView(viewsets.ViewSet):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def get(self, request):

        try:
            if request.user.hospital_profile is None:
                return Response(status=status.HTTP_200_OK)

            queryset = Requirement.objects.filter(hospital=request.user.hospital_profile)
            serializer = CreateRequirementSerializer(queryset, many=True)
            return Response(serializer.data)

        except Requirement.DoesNotExist:
            return Response(status=status.HTTP_200_OK)

    def post(self, request):

        if request.user.hospital_profile is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = CreateRequirementSerializer(data=request.data, context={'user': request.user})
        if not serializer.is_valid():
            return Response(serializer.errors)
        serializer.save()

        return Response(serializer.data)

class VendorStockView(viewsets.ViewSet):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def get(self, request):

        try: 
            vendor_profile = request.user.vendor_profile 
        except VendorProfile.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            queryset = Stock.objects.filter(vendor=request.user.vendor_profile)
            serializer = CreateStockSerializer(queryset, many=True)
            return Response(serializer.data)

        except Requirement.DoesNotExist:
            return Response(status=status.HTTP_200_OK)

    def post(self, request):

        try: 
            vendor_profile = request.user.vendor_profile 
        except VendorProfile.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = CreateStockSerializer(data=request.data, context={'user': request.user})
        if not serializer.is_valid():
            return Response(serializer.errors)
        serializer.save()

        return Response(serializer.data)

class StockViewList(mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """
    Updates and retrieves user accounts
    """
    
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = (AllowAny,)

class RequirementViewList(mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """
    Updates and retrieves user accounts
    """
    
    queryset = Requirement.objects.all()
    serializer_class = RequirementSerializer
    permission_classes = (AllowAny,)
    