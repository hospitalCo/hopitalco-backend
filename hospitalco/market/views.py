from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import ItemSerializer, RequirementSerializer
from .models import Item, Requirement

class ItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Items to be viewed or edited.
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated]

class RequirementViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Requirements to be viewed or edited.
    """
    queryset = Requirement.objects.all()
    serializer_class = RequirementSerializer
    permission_classes = [permissions.IsAuthenticated]
