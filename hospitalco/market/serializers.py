from rest_framework import serializers

from .models import Category, Item, Requirement


class ItemSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Item
        fields = ["id", "name", "details", "category"]


class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirement
        fields = ["id", "user", "item", "quantity"]


class CategorySerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = Category
        fields = ("id", "name", "items")
