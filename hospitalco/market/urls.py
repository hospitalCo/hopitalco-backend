from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ItemViewSet, RequirementViewSet

router_category = DefaultRouter()
router_category.register(r"categories", CategoryViewSet)

router_item = DefaultRouter()
router_item.register(r"items", ItemViewSet)

router_requirement = DefaultRouter()
router_requirement.register(r"requirements", RequirementViewSet)

urlpatterns = [
    path("", include(router_category.urls)),
    path("", include(router_item.urls)),
    path("", include(router_requirement.urls)),
]
