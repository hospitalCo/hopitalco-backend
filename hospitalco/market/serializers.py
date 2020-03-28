from django.contrib.auth.models import Group
from rest_framework import serializers

from .models import Item, Requirement


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "name", "details"]


class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirement
        fields = ["id", "user", "items", "quantity"]
