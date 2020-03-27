from django.urls import path, re_path, include
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from .views import UserRegisterViewSet, UserListSet, UserLoginView, \
    UserDetailsView, HospitalViewSet, VendorViewSet, UserHospitalView, \
    UserLogoutView, UserVendorView

router_users = DefaultRouter()
router_users.register(r'register', UserRegisterViewSet)
router_users.register(r'hospitals', HospitalViewSet)
router_users.register(r'', UserListSet)

router_hospitals = DefaultRouter()
router_hospitals.register(r'', HospitalViewSet)

router_vendors = DefaultRouter()
router_vendors.register(r'', VendorViewSet)

urlpatterns = [
    path('users/', include(router_users.urls)),
    path('users/login/', UserLoginView.as_view()),
    path('users/logout/', UserLogoutView.as_view()),
    path('users/me/', UserDetailsView.as_view()),
    path('users/me/hospital/', UserHospitalView.as_view({'get' : 'get', 'post' : 'post'})),
    path('users/me/vendor/', UserVendorView.as_view({'get' : 'get', 'post' : 'post'})),
    path('hospitals/', include(router_hospitals.urls)),
    path('vendors/', include(router_vendors.urls)),
]