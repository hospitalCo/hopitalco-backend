from django.db import models
from hospitalco.users.models import User

# Create your models here.

class Item(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100,unique=True, blank=False)
    details = models.TextField(blank=True)
    class Meta:
        ordering = ['name']

class Requirement(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items =  models.ManyToManyField(Item, related_name='itemsReq',)
    quantity = models.PositiveIntegerField()
    class Meta:
        ordering = ['user']

