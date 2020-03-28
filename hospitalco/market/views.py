from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from .serializers import ItemSerializer, RequirementSerializer
from .models import Item, Requirement
from hospitalco.users.views import CsrfExemptSessionAuthentication

class ItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Items to be viewed or edited.
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (CsrfExemptSessionAuthentication,)

class RequirementViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Requirements to be viewed or edited.
    """
    queryset = Requirement.objects.all()
    serializer_class = RequirementSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def create(self, request):
        item = Item.objects.get(pk=1)
        user = request.user
        req = Requirement(user=user, quantity= 10)

        req.save()
        req.items.add(item)

        return Response({'status': request.user.username}) 
