from django.contrib.auth import login, logout
from rest_framework import mixins, status, views, viewsets
from rest_framework.authentication import SessionAuthentication, authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import HospitalProfile, User, VendorProfile
from .serializers import (
    CreateHospitalSerializer,
    CreateUserSerializer,
    CreateVendorSerializer,
    HospitalProfileSerializer,
    UserSerializer,
    VendorProfileSerializer,
)


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class UserRegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
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
        username = data.get("username", None)
        password = data.get("password", None)

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


class UserListSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Updates and retrieves user accounts
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class HospitalViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Updates and retrieves user accounts
    """

    queryset = HospitalProfile.objects.all()
    serializer_class = HospitalProfileSerializer
    permission_classes = (AllowAny,)


class VendorViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
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

        serializer = CreateHospitalSerializer(data=request.data, context={"user": request.user})
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

        serializer = CreateVendorSerializer(data=request.data, context={"user": request.user})
        if not serializer.is_valid():
            return Response(serializer.errors)
        serializer.save()

        return Response(serializer.data)
