from django.core.validators import MinValueValidator
from django.db import models
from hospitalco.users.models import User

# Create your models here.


class Category(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, unique=True, blank=False)

    class Meta:
        ordering = ["name"]


class Item(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, unique=True, blank=False)
    details = models.TextField(blank=True)
    category = models.ForeignKey(Category, null=False, on_delete=models.CASCADE, related_name="items")

    class Meta:
        ordering = ["name"]


class Requirement(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name="requirements", on_delete=models.PROTECT)
    quantity = models.DecimalField(
        decimal_places=3, max_digits=10, validators=[MinValueValidator(limit_value=0)]
    )
    fullfilled_at = models.DateTimeField(blank=False, null=True)

    class Meta:
        ordering = ["user"]
