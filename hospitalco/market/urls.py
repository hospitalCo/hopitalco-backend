from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ItemViewSet, RequirementViewSet

router_Item = DefaultRouter()
router_Item.register(r"items", ItemViewSet)
router_requirement = DefaultRouter()
router_requirement.register(r"requirements", RequirementViewSet)

urlpatterns = [
    path("", include(router_Item.urls)),
    path("", include(router_requirement.urls)),
]
